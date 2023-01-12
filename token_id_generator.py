import pickle


class TokenIdGenerator:
    """
    Generates a unique index for tokens, as well as allows you to get an index on a token, a token on an index, etc.
    """
    def __init__(self):
        self.current_id = 0
        self.token_to_id = {}
        self.id_to_value = {}
        self.id_to_type = {}

    def get_id_by_token(self, token):
        """
        Returns the index by token
        :param token: dict
            {
                "value": value,
                "type": type
            }
        :return: int
            token id
        """
        token_value = token["value"]
        token_type = token["type"]
        if token_value in self.token_to_id:
            return self.token_to_id[token_value]
        else:
            self.current_id += 1
            self.token_to_id[token_value] = self.current_id
            self.id_to_value[self.current_id] = token_value
            self.id_to_type[self.current_id] = token_type
        return self.current_id

    def get_id_by_value(self, value):
        """
        Get id by value or -1 if there is no value
        :param value: str
        :return: int
            token id
        """
        if value in self.token_to_id:
            return self.token_to_id[value]
        return -1

    def contains(self, token_id):
        """
        Check that the id is contained in the generator
        :param token_id: int
        :return: bool
        """
        if token_id in self.id_to_value:
            return True
        else:
            return False

    def get_value(self, token_id):
        """
        Get the value from the index
        :param token_id: int
        :return: str or None
        """
        if self.contains(token_id):
            return self.id_to_value[token_id]
        else:
            return None

    def get_type(self, token_id):
        """
        Get the type by index
        :param token_id: int
        :return: str or None
        """
        if self.contains(token_id):
            return self.id_to_type[token_id]
        else:
            return None

    def load(self, path):
        """
        Loading the generator with Pickle
        :param path: str
        :return: TokenIdGenerator
        """
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.__dict__.update(data.__dict__)
        return self

    def dump(self, path):
        """
        Saving the generator with Pickle
        :param path: str
        :return: None
        """
        with open(path, "wb") as f:
            pickle.dump(self, f)
