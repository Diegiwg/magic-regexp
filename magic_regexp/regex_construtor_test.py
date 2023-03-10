from regex_construtor import Flags, RegexConstrutor, Atalho, ClasseCaracteres, Intervalo, Quantificador

rc = RegexConstrutor()

# Exemplo: CPF Simples - 000.000.000-00 ou 11111111111
print(
    (
        rc.exatamente_n(3, Atalho.NUMERO)
        .zero_ou_um('.')
        .exatamente_n(3, Atalho.NUMERO)
        .zero_ou_um('.')
        .exatamente_n(3, Atalho.NUMERO)
        .zero_ou_um('-')
        .exatamente_n(2, Atalho.NUMERO)
        .construir(Flags.ASCII)
    ).findall(
        """
    Esse é um CPF com pontuação: 000.000.000-00;
    Já esse, não tem rs: 11111111111;
    E esse tem simbolos invalidos: 222-222-222.22;
"""
    )
)
# Saida: RegexBuilder::debug --> re.compile('\\d{3}.?\\d{3}.?\\d{3}-?\\d{2}', re.ASCII)
#        ['000.000.000-00', '11111111111']


# Exemplo: intervalo
print(
    (
        rc.um_ou_mais(ClasseCaracteres([Intervalo('1', '5')]))
        .termina_com('a')
        .construir(Flags.MULTILINE)
    ).findall(
        """
        111a

        as[a]5555a
        """
    )
)
# Saida: RegexBuilder::debug --> re.compile('[1-5]+a$', re.MULTILINE)
#        ['111a', '5555a']

# Exemplo: intervalo
print(
    (
        rc.comeca_com(Quantificador(1, None, Atalho.ESPACO))
        .um_ou_mais('abc')
        .um_ou_mais(ClasseCaracteres([Intervalo('1', '5'), Atalho.NAO_NUMERO]))
        .termina_com('5')
        .construir()
    ).findall('  abcabc123xyz.5')
)
# Saida: RegexBuilder::debug --> re.compile('^\\s+(?:abc)+[1-5\\D]+5$')
#        ['  abcabc123xyz.5']
