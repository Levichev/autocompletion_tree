import pickle


class TreeNode:
    def __init__(self, id_token):
        self.id_token = id_token
        self.token_count = 1
        self.children = {}
    
    def write_branch_to_tree(self, tokens, id_generator):
        current_node = self
        for token in tokens:
            id_token = id_generator.get_id_by_token(token)
            if id_token in current_node.children:
                current_node = current_node.children[id_token]
                current_node.token_count += 1
            else:
                new_node = TreeNode(id_token)
                current_node.children[id_token] = new_node
                current_node = new_node

    def load(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.__dict__.update(data.__dict__)
        return self

    def dump(self, path):
        with open(path, "wb") as f:
            pickle.dump(self, f)
