import os


def test(path, root_node, id_generator, func, max_file_count=100, max_tokens=10, top_n=1):
    processed_files_count = 0
    count_true = 0
    count_false = 0
    count_true_whitespace_or_newline = 0
    percent = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.java'):
                result = func(root, file, root_node, id_generator, max_tokens, top_n)
                count_true += result["count_true"]
                count_false += result["count_false"]
                count_true_whitespace_or_newline += result["count_true_whitespace_or_newline"]
                processed_files_count += 1

                percent = count_true / (count_true + count_false) if count_true + count_false > 0 else 0
                print(f"\rprocessed files {processed_files_count}: {round(percent * 100, 2)}%", end='')

        if processed_files_count >= max_file_count:
            break

    print()
    return {
        "processed_files_count": processed_files_count,
        "percent": percent,
        "count_true": count_true,
        "count_false": count_false,
        "count_true_whitespace_or_newline": count_true_whitespace_or_newline
    }
