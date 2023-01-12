from tokenize_all import Java


def tokenize_java_code(code):
    """
    Tokenizes lines of java code
    :param code: str
    :return: list
        {"value": value, "type": type}
    """
    tok = []
    try:
        tokens = Java.tokenize(code)

        for token in tokens:
            if token.type == "comment":
                continue
            tok.append({"value": token.value, "type": token.type})
        return tok
    except Exception as e:
        return []
