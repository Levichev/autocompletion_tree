import os

from tokenizer import tokenize_java_code


def get_token_from_file(root, file):
    with open(os.path.join(root, file), 'r', encoding="utf-8", errors='ignore') as f:
        line = f.readline()
        tokens = []
        while line:
            line = line[0:-1]
            tokenized_line = tokenize_java_code(line)
            tokens += tokenized_line
            tokens.append({"value": "\n", "type": "newline"})

            line = f.readline()
    return tokens


        
def write_branch_to_tree(node, id_tokens, start_index, id_generator, max_tokens):
    node.write_branch_to_tree(id_tokens[start_index:start_index+max_tokens], id_generator)


def train_model_all_string(root, file, root_node, id_generator, max_tokens):
    tokens = get_token_from_file(root, file)

    for start_index in range(len(tokens)):
        write_branch_to_tree(root_node, tokens, start_index, id_generator, max_tokens)


def get_next_tokens_i(node, id_generator, tokens, count_returned_tokens, i):
    returned_tokens = []
    while i < len(tokens):
        id_tokens = id_generator.get_id_by_token(tokens[i])
        if id_tokens in node.children:
            node = node.children[id_tokens]
            i += 1
        else:
            break

    if i == len(tokens):
        children = sorted(list([
            node.children[x].token_count, 
            id_generator.get_value(node.children[x].id_token)
        ] for x in node.children), reverse=True)
        
        returned_tokens += children[:count_returned_tokens]
    return returned_tokens


def get_next_tokens(root_node, max_depth, id_generator, tokens, count_returned_tokens):
    
    returned_tokens = []
    for i in range(max(0, len(tokens)-max_depth), len(tokens)):
        next_tokens = get_next_tokens_i(root_node, id_generator, tokens, count_returned_tokens, i)
        returned_tokens += next_tokens
        if len(next_tokens) > 0:
            break
    
    return returned_tokens


def get_next_n_tokens(root_node, max_depth, id_generator, tokens, count_returned_tokens, n):
    return_tokens = []

    while n >= 2:
        next_token = get_next_tokens(root_node, max_depth, id_generator, tokens, 1)
        if len(next_token) != 0:
            value = next_token[0][1]
            token_id = id_generator.get_id_by_value(value)
            tokens.append({"value": value, "type": id_generator.get_type(token_id)})
            return_tokens += next_token
        else:
            break
        n -= 1
    if n == 1:
        next_token = get_next_tokens(root_node, max_depth, id_generator, tokens, count_returned_tokens)
        if len(next_token) != 0:
            tmp = return_tokens
            return_tokens = []
            for x in next_token:
                return_tokens.append(tmp + [x])

    return return_tokens

    
def test_model(root, file, node, id_generator, max_tokens, top_n):
    tokens = get_token_from_file(root, file)

    count_true = 0
    count_true_whitespace_or_newline = 0
    count_false = 0
    for i, token in enumerate(tokens):
        test_tokens = tokens[i:i+max_tokens]

        returned_tokens = get_next_tokens(node, max_tokens, id_generator, test_tokens[:-1], top_n)  
        
        flag = any(x[1] == test_tokens[-1]["value"] for x in returned_tokens)
        
        if flag:
            if test_tokens[-1]["type"] not in ["whitespace", "newline"]:
                count_true += 1
            else:
                count_true_whitespace_or_newline += 1
        else:
            count_false += 1

    return {
        'count_true': count_true, 
        'count_false': count_false,
        'count_true_whitespace_or_newline':count_true_whitespace_or_newline
    }

