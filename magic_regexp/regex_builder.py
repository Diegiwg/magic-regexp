import re
from enum import Enum
from typing import Any, Union


class CharacterSpecialTypes(Enum):
    QUALQUER = r'.'
    DIGITO = r'\d'
    NAO_DIGITO = r'\D'
    ESPACO_EM_BRANCO = r'\s'
    NAO_ESPACO_EM_BRANCO = r'\S'
    ALFA = r'\w'
    NAO_ALFA = r'\W'

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


class CharacterInterval:
    def __init__(self, inicio: Any, fim: Any) -> None:
        self.start = inicio
        self.end = fim

    def __repr__(self) -> str:
        return f'[{self.start}-{self.end}]'

    def __str__(self) -> str:
        return f'[{self.start}-{self.end}]'


class CharacterGroup:
    def __init__(
        self, *group: Union[str, CharacterSpecialTypes, CharacterInterval]
    ) -> None:
        m_group_parsed = str()

        for g in group:
            m_group_parsed += str(g)

        self.group = m_group_parsed

    def __repr__(self) -> str:
        return f'[{self.group}]'

    def __str__(self) -> str:
        return f'[{self.group}]'


class Token:
    def __init__(
        self, token_value: Union[str, CharacterSpecialTypes, CharacterGroup]
    ) -> None:
        self.value: Union[
            str, CharacterSpecialTypes, CharacterGroup
        ] = token_value

    def __repr__(self) -> str:
        return f'{self.value}'

    def __str__(self) -> str:
        return f'{self.value}'


class RegexBuilder:
    def __init__(self, debug: bool = False) -> None:
        self._debugging: bool = debug
        self._tokens: list[str] = []

    def _escape_special_characters(self, token: str) -> str:
        """
        >>> rb = RegexBuilder()

        >>> token = str(Token('Test'))
        >>> rb._escape_special_characters(token)
        'Test'

        >>> token = str(Token(CharacterSpecialTypes.DIGITO))
        >>> rb._escape_special_characters(token)
        '\\\\d'

        >>> token = str(Token(CharacterInterval(inicio='1', fim='9')))
        >>> rb._escape_special_characters(token)
        '1-9'
        """

        return token.replace('[', '').replace(']', '')

    def construir(self) -> re.Pattern[str]:
        """
        Constrói um padrão de regex a partir do conjunto de tokens anteriomente configurados.

        Examples:
            >>> rb = RegexBuilder()
            >>> rb.construir()
            re.compile('')
        """

        m_tokens_string: str = ''.join(self._tokens)
        m_compiled_regex: re.Pattern[str] = re.compile(m_tokens_string)

        self._tokens.clear()  # Clear tokens list for reusability
        return m_compiled_regex

    def contenha(
        self, token: Union[str, CharacterSpecialTypes, CharacterGroup]
    ):
        """
        Adiciona o token passado como match direto.

        Args:
            token: Token para dar match direto.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.contenha('Test').construir()
            re.compile('Test')

            >>> rb.contenha(CharacterSpecialTypes.QUALQUER).construir()
            re.compile('.')

            >>> rb.contenha(CharacterInterval(inicio='a', fim='b')).construir()
            re.compile('[a-b]')

            >>> rb.contenha(CharacterGroup('abc')).construir()
            re.compile('[abc]')
        """
        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        self._tokens.append(m_parsed_token)
        return self

    def nao_contenha(
        self, token: Union[str, CharacterSpecialTypes, CharacterGroup]
    ):
        """
        Adiciona o token passado como não esperado para dar match.

        Args:
            token: Token para dar não dar match.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.nao_contenha('Test').construir()
            re.compile('[^Test]')

            >>> rb.nao_contenha(CharacterSpecialTypes.DIGITO).construir()
            re.compile('[^\\\\d]')

            >>> rb.nao_contenha(CharacterInterval(inicio='a', fim='b')).construir()
            re.compile('[^a-b]')

            >>> rb.nao_contenha(CharacterGroup('abc')).construir()
            re.compile('[^abc]')
        """
        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        m_escaped_token = self._escape_special_characters(m_parsed_token)

        self._tokens.append('[^' + m_escaped_token + ']')
        return self

    def comeca_com(
        self, token: Union[str, CharacterSpecialTypes, CharacterGroup]
    ):
        """
        Adiciona o token passado como esperado no inicio da linha.

        Args:
            token: Token para esperado no inicio da linha.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.comeca_com('Test').construir()
            re.compile('^Test')

            >>> rb.comeca_com(CharacterSpecialTypes.DIGITO).construir()
            re.compile('^\\\\d')

            >>> rb.comeca_com(CharacterInterval(inicio='0', fim='5')).construir()
            re.compile('^[0-5]')

            >>> rb.comeca_com(CharacterGroup('abc')).construir()
            re.compile('^[abc]')
        """
        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        self._tokens.append('^' + m_parsed_token)
        return self

    def termina_com(
        self, token: Union[str, CharacterSpecialTypes, CharacterGroup]
    ):
        """
        Adiciona o token passado como esperado no fim da linha.

        Args:
            token: Token esperado no fim da linha.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.termina_com('Test').construir()
            re.compile('Test$')

            >>> rb.termina_com(CharacterSpecialTypes.DIGITO).construir()
            re.compile('\\\\d$')

            >>> rb.termina_com(CharacterInterval(inicio='0', fim='5')).construir()
            re.compile('[0-5]$')

            >>> rb.termina_com(CharacterGroup('abc')).construir()
            re.compile('[abc]$')
        """
        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        self._tokens.append(m_parsed_token + '$')
        return self

    def zero_ou_uma(
        self, token: Union[str, CharacterSpecialTypes, CharacterGroup]
    ):
        """
        Adiciona o token passado como esperado zero ou uma vez.

        Args:
            token: Token esperado zero ou uma vez.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.zero_ou_uma('0').construir()
            re.compile('0?')

            >>> rb.zero_ou_uma(CharacterSpecialTypes.DIGITO).construir()
            re.compile('\\\\d?')

            >>> rb.zero_ou_uma(CharacterInterval(inicio='0', fim='5')).construir()
            re.compile('[0-5]?')

            >>> rb.zero_ou_uma(CharacterGroup('abc')).construir()
            re.compile('[abc]?')
        """
        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        self._tokens.append(f'{m_parsed_token}?')
        return self

    def zero_ou_mais(
        self, token: Union[str, CharacterSpecialTypes, CharacterGroup]
    ):
        """
        Adiciona o token passado como esperado zero ou mais vezes.

        Args:
            token: Token esperado zero ou mais vezes.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.zero_ou_mais('0').construir()
            re.compile('0*')

            >>> rb.zero_ou_mais(CharacterSpecialTypes.DIGITO).construir()
            re.compile('\\\\d*')

            >>> rb.zero_ou_mais(CharacterInterval(inicio='0', fim='5')).construir()
            re.compile('[0-5]*')

            >>> rb.zero_ou_mais(CharacterGroup('abc')).construir()
            re.compile('[abc]*')
        """

        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        self._tokens.append(f'{m_parsed_token}*')
        return self

    def uma_ou_mais(
        self, token: Union[str, CharacterSpecialTypes, CharacterGroup]
    ):
        """
        Adiciona o token passado como esperado uma ou mais vezes.

        Args:
            token: Token esperado uma ou mais vezes.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.uma_ou_mais('0').construir()
            re.compile('0+')

            >>> rb.uma_ou_mais(CharacterSpecialTypes.DIGITO).construir()
            re.compile('\\\\d+')

            >>> rb.uma_ou_mais(CharacterInterval(inicio='0', fim='5')).construir()
            re.compile('[0-5]+')

            >>> rb.uma_ou_mais(CharacterGroup('abc')).construir()
            re.compile('[abc]+')
        """

        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        self._tokens.append(f'{m_parsed_token}+')
        return self

    def exatamente_n(
        self,
        vezes: int,
        token: Union[str, CharacterSpecialTypes, CharacterGroup],
    ):
        """
        Adiciona o token passado como esperado n vezes.

        Args:
            vezes: Número de vezes esperado.
            token: Token esperado n vezes.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.exatamente_n(2, '0').construir()
            re.compile('0{2}')

            >>> rb.exatamente_n(2, CharacterSpecialTypes.DIGITO).construir()
            re.compile('\\\\d{2}')

            >>> rb.exatamente_n(2, CharacterInterval(inicio='0', fim='5')).construir()
            re.compile('[0-5]{2}')

            >>> rb.exatamente_n(2, CharacterGroup('abc')).construir()
            re.compile('[abc]{2}')
        """

        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        self._tokens.append(m_parsed_token + '{' + str(vezes) + '}')
        return self

    def n_ou_mais(
        self,
        vezes: int,
        token: Union[str, CharacterSpecialTypes, CharacterGroup],
    ):
        """
        Adiciona o token passado como esperado n ou mais vezes.

        Args:
            vezes: Número de vezes esperado.
            token: Token esperado n ou mais vezes.

        Examples:
            >>> rb = RegexBuilder()

            >>> rb.n_ou_mais(2, '0').construir()
            re.compile('0{2,}')

            >>> rb.n_ou_mais(2, CharacterSpecialTypes.DIGITO).construir()
            re.compile('\\\\d{2,}')

            >>> rb.n_ou_mais(2, CharacterInterval(inicio='0', fim='5')).construir()
            re.compile('[0-5]{2,}')

            >>> rb.n_ou_mais(2, CharacterGroup('abc')).construir()
            re.compile('[abc]{2,}')
        """

        m_token: Token = Token(token)
        m_parsed_token: str = str(m_token)

        self._tokens.append(m_parsed_token + '{' + str(vezes) + ',' + '}')
        return self
