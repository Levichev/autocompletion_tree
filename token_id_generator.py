import pickle


class TokenIdGenerator:
    def __init__(self):
        self.current_id = 0
        self.token_to_id = {}
        self.id_to_value = {}
        self.id_to_type = {}

    def get_id_by_token(self, token):
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
        if value in self.token_to_id:
            return self.token_to_id[value]
        return -1

    def contains(self, token_id):
        if token_id in self.id_to_value:
            return True
        else:
            return False

    def get_value(self, token_id):
        if self.contains(token_id):
            return self.id_to_value[token_id]
        else:
            return None

    def get_type(self, token_id):
        if self.contains(token_id):
            return self.id_to_type[token_id]
        else:
            return None

    def load(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.__dict__.update(data.__dict__)
        return self

    def dump(self, path):
        with open(path, "wb") as f:
            pickle.dump(self, f)
