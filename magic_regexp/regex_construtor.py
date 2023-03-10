import re
from enum import Enum
from typing import Any, Callable, Union, Optional, List


def debug(msg: Any):
    print(f'RegexBuilder::debug --> {msg}')

class Atalho(Enum):
    QUALQUER_CARACTERE = '.'
    # embora assim "funcione", melhor usar raw string para não confundir com sequência de escape
    NUMERO = r'\d'
    NAO_NUMERO = r'\D'
    ALFANUM = r'\w' # mudei o nome porque \w é letra, número ou _
    NAO_ALFANUM = r'\W'
    ESPACO = r'\s' # vale lembrar que \s também pega TAB e quebra de linha
    NAO_ESPACO = r'\S'
    def __str__(self):
        return self.value
    def __len__(self):
        return 1 # todos os atalhos contam como 1 token

class ParteClasseCaracteres:
    def __init__(self, valor: Any):
        self.valor = valor

    def __str__(self):
        if isinstance(self.valor, str):
            return re.escape(self.valor)
        elif isinstance(self.valor, Atalho):
            return self.valor.value
        return str(self.valor)

class Intervalo:
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim

    def __str__(self):
        return f'{self.inicio}-{self.fim}'

class ClasseCaracteres:
    def __init__(self, partes: List[Union[ParteClasseCaracteres, Intervalo]], negated: bool = False):
        self.partes = partes
        self.negated = negated

    def add(self, parte: ParteClasseCaracteres):
        self.partes.append(parte)

    def __str__(self):
        return '[' + ('^' if self.negated else '') + ''.join(str(p) for p in self.partes) + ']'
    def __len__(self):
        return 1 # toda classe de caracteres conta como 1 token (pois corresponde a apenas um caractere)

class Flags(Enum):
    ASCII = re.ASCII
    IGNORECASE = re.IGNORECASE
    MULTILINE = re.MULTILINE
    DOTALL = re.DOTALL

# mais informações em:
# - https://www.rexegg.com/regex-quantifiers.html
# - https://www.regular-expressions.info/repeat.html
class TipoQuantificador(Enum):
    GREEDY = ''
    LAZY = '?'
    # se estiver usando Python >= 3.11, pode descomentar esse aqui
    # explicação em https://www.regular-expressions.info/possessive.html
    # POSSESSIVE = '+'
    def __str__(self):
        return self.value

class Ancora(Enum):
    # se a flag MULTILINE está ligada, eles também pegam início e fim de linha
    INICIO_STRING_OU_LINHA = '^'
    FIM_STRING_OU_LINHA = '$'
    def __str__(self):
        return self.value

def flags_parser(data: Any):
    flags = 0
    for flag in data:
        flags |= flag.value
    return flags

# se max for None, indica que não tem limite máximo
# capture indica se o texto ficará em um grupo de captura
class Quantificador:
    def __init__(self, minimo: int, maximo: Optional[int], valor: Any,
                 tipo: TipoQuantificador = TipoQuantificador.GREEDY, capture: bool = False):
        # quantidades inválidas: algum valor é menor que zero, ou max é menor que min, ou ambos são zero
        if minimo < 0 or (maximo is not None and (maximo < 0 or maximo < minimo or (maximo == 0 and minimo == 0))):
            raise ValueError('Quantidades inválidas') # depois pode melhorar esta mensagem
        self.min = minimo
        self.max = maximo
        self.tipo = tipo
        self.capture = capture
        self.valor = valor

    def __str__(self):
        # se o texto tiver mais que um caractere, precisa de parênteses
        # por exemplo, abc+ só repete o "c", mas se for para repetir tudo, tem que ser (abc)+
        # e uso re.escape para escapar os caracteres especiais
        if len(self.valor) == 1:
            texto = str(self.valor)
        else:
            texto = '(' + ('' if self.capture else '?:') + f'{str(self.valor)})'

        if self.min == self.max:
            return f'{texto}{{{self.min}}}{self.tipo.value}'
        elif self.min == 0:
            if self.max == 1:
                return f'{texto}?{self.tipo.value}'
            elif self.max is None:
                return f'{texto}*{self.tipo.value}'
            else:
                return f'{texto}{{{self.min},{self.max}}}{self.tipo.value}'
        elif self.min == 1:
            if self.max is None:
                return f'{texto}+{self.tipo.value}'
            else:
                return f'{texto}{{{self.min},{self.max}}}{self.tipo.value}'
        else:
            if self.max is None:
                return f'{texto}{{{self.min},}}{self.tipo.value}'
            else:
                return f'{texto}{{{self.min},{self.max}}}{self.tipo.value}'

class RegexToken:
    def __init__(self, valor: Union[str, Atalho, Ancora, Quantificador, ClasseCaracteres]):
        self.valor = valor

    def is_str(self):
        return isinstance(self.valor, str)

    def __len__(self):
        if isinstance(self.valor, str):
            return len(self.valor)
        return len(str(self.valor))

    def __str__(self):
        if isinstance(self.valor, str):
            return re.escape(self.valor)
        if isinstance(self.valor, (Atalho, Ancora)):
            return self.valor.value
        return str(self.valor)


class RegexConstrutor:
    def __init__(self):
        self._tokens = []

    def _to_token(self, valor: Any):
        if isinstance(valor, (str, Atalho, Ancora, Quantificador, ClasseCaracteres)):
            return RegexToken(valor)
        if isinstance(valor, (ParteClasseCaracteres, Intervalo)):
            return RegexToken(ClasseCaracteres(valor))
        return valor

    def contenha(self, valor: Union[str, RegexToken]):
        self._tokens.append(self._to_token(valor))
        return self

    def comeca_com(self, valor: Union[str, RegexToken]):
        self._tokens.append(RegexToken(Ancora.INICIO_STRING_OU_LINHA))
        self._tokens.append(self._to_token(valor))
        return self

    def termina_com(self, valor: Union[str, RegexToken]):
        self._tokens.append(self._to_token(valor))
        self._tokens.append(RegexToken(Ancora.FIM_STRING_OU_LINHA))
        return self

    def zero_ou_um(self, valor: Union[str, RegexToken], tipo: TipoQuantificador = TipoQuantificador.GREEDY, capture: bool = False):
        self._tokens.append(RegexToken(Quantificador(0, 1, self._to_token(valor), tipo, capture)))
        return self

    def zero_ou_mais(self, valor: Union[str, RegexToken], tipo: TipoQuantificador = TipoQuantificador.GREEDY, capture: bool = False):
        self._tokens.append(RegexToken(Quantificador(0, None, self._to_token(valor), tipo, capture)))
        return self

    def um_ou_mais(self, valor: Union[str, RegexToken], tipo: TipoQuantificador = TipoQuantificador.GREEDY, capture: bool = False):
        self._tokens.append(RegexToken(Quantificador(1, None, self._to_token(valor), tipo, capture)))
        return self

    def exatamente_n(self, vezes: int, valor: Union[str, RegexToken], tipo: TipoQuantificador = TipoQuantificador.GREEDY, capture: bool = False):
        self._tokens.append(RegexToken(Quantificador(vezes, vezes, self._to_token(valor), tipo, capture)))
        return self

    def n_ou_mais(self, vezes: int, valor: Union[str, RegexToken], tipo: TipoQuantificador = TipoQuantificador.GREEDY, capture: bool = False):
        self._tokens.append(RegexToken(Quantificador(vezes, None, self._to_token(valor), tipo, capture)))
        return self

    def construir(self, *flags: Flags):
        regex = re.compile(
            ''.join(map(str, self._tokens)),
            flags_parser(flags),
        )
        self._tokens = []

        debug(regex)
        return regex
