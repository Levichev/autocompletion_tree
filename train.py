import os

from tree_node import TreeNode
from token_id_generator import TokenIdGenerator


def train(path, func, max_file_count=100, max_tokens=10):
    root_node = TreeNode("")

    cnt = 0
    id_generator = TokenIdGenerator()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.java'):
                func(root, file, root_node, id_generator, max_tokens)
                cnt += 1
                print(f"\rprocessed files: {cnt}", end='')

        if cnt >= max_file_count:
            break
    print()

    return {"id_generator": id_generator, "root_node": root_node}


def train_for_count_test(path, func, max_file_count, max_tokens):
    root_node = TreeNode("")
    id_generator = TokenIdGenerator()

    cnt = 0
    i = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.java'):
                func(root, file, root_node, id_generator, max_tokens)
                cnt += 1
                print(f"\rprocessed files: {cnt}", end='')

        if cnt >= max_file_count[i]:
            model_path = f"trained_models/tree{max_file_count[i]}_{max_tokens}.pkl"
            id_generator_path = f"trained_models/id{max_file_count[i]}_{max_tokens}.pkl"
            root_node.dump(model_path)
            id_generator.dump(id_generator_path)    
            i += 1
            print(f"\nDump: {model_path}, {id_generator_path}")
            if i >= len(max_file_count):
                break
    print()

    return {"id_generator": id_generator, "root_node": root_node}
