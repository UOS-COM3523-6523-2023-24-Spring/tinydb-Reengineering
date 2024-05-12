def get_k_tail(text, k):
    """
    从文本中获取长度为 k 的后缀列表
    """
    tails = []
    for i in range(len(text) - k + 1):
        tail = text[i:i+k]
        tails.append(tail)
    return tails


def find_similarities(file1_path, file2_path, k):
    """
    查找两个文件中的相似后缀
    """
    with open(file1_path, 'r') as file1:
        content1 = file1.read()
    with open(file2_path, 'r') as file2:
        content2 = file2.read()

    tails1 = get_k_tail(content1, k)
    tails2 = get_k_tail(content2, k)

    similarities = []
    for tail1 in tails1:
        if tail1 in tails2 and tail1 not in similarities:
            similarities.append(tail1)

    return similarities




file_paths = ['database.py', 'middlewares.py', 'mypy_plugin.py', 'operations.py', 'queries.py', 'storages.py', 'table.py', 'utils.py', 'version.py']
k = 12

output_file = 'similarities.txt'

with open(output_file, 'w') as file:
    for i in range(len(file_paths)):
        for j in range(i + 1, len(file_paths)):
            file1_path = file_paths[i]
            file2_path = file_paths[j]

            similarities = find_similarities(file1_path, file2_path, k)

            if similarities:
                file.write("Similarities between {} and {} (k-tail length: {}):\n".format(file1_path, file2_path, k))
                file.write("===============================\n")
                for similarity in similarities:
                    file.write(similarity + '\n')
                file.write("===============================\n")
            else:
                file.write("No similarities found between {} and {} (k-tail length: {}).\n".format(file1_path, file2_path, k))