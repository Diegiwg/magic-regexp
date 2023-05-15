import re


class Builder:
    def __init__(self):
        self.__products = []

    def token(self, token):
        self.__products.append(token)
        return self

    def character(self, token):
        self.__products.append("[" + token + "]")
        return self

    def is_optional(self):
        self.__products.append("?")
        return self

    def start(self):
        self.__products.append("^")
        return self

    def end(self):
        self.__products.append("$")
        return self

    def open_group(self):
        self.__products.append("(")
        return self

    def close_group(self):
        self.__products.append(")")
        return self

    def or_token(self):
        self.__products.append("|")
        return self

    def n_times(self, times, token):
        self.__products.append(token + "{" + str(times) + "}")
        return self

    def range_times(self, min, max, token):
        self.__products.append(token + "{" + str(min) + "," + str(max) + "}")
        return self

    def n_or_more(self, times: int, token):
        self.__products.append(token + "{" + str(times) + ",}")
        return self

    def one_or_more(self, token):
        self.__products.append(token + "+")
        return self

    def build(self):
        pattern = "".join(self.__products)
        self.__products = []
        return re.compile(pattern)
