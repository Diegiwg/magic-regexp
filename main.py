from lib.builder import Builder

builder = Builder()

patterns = [
    # regex que valida se é uma string simples
    builder.start().token("[a-zA-Z0-9]+").end().build(),
    # regex que valida se uma string é um email
    builder.start()
    .one_or_more("[a-zA-Z0-9._%+-]")
    .character("@")
    .one_or_more("[a-zA-Z0-9.-]")
    .character(".")
    .n_or_more(2, "[a-zA-Z]")
    .end()
    .build(),
    # regex que valida se uma string é um número de telefone válido com código de área
    builder.start()
    .open_group()
    .character("(")
    .n_times(2, "\d")
    .character(")")
    .or_token()
    .n_times(2, "\d")
    .close_group()
    .character("\s")
    .is_optional()
    .range_times(4, 5, "\d")
    .character("-")
    .n_times(4, "\d")
    .end()
    .build(),
    # regex que valida se uma string é uma senha forte
    builder.start()
    .open_group()
    .token("(?=.*[A-Z])")
    .token("(?=.*[a-z])")
    .token("(?=.*\d)")
    .token("(?=.*[!@#$%^&*()_+\-=[\]{};':\\|,.<>/?])" + '"')
    .close_group()
    .n_or_more(8, ".")
    .end()
    .build(),
]
tests = ["AbCd223", "usuario@dominio.cc", "(11) 1111-1111", "P@ssw0rd!"]
for test, pattern in enumerate(patterns):
    print(tests[test], "->", pattern)
    print(pattern, "->", pattern.match(tests[test]))
    print()
