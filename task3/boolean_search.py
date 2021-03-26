import re


def read_index():
    f = open("index.txt", "r")
    lines = f.readlines()
    index = dict()
    for line in lines:
        words = re.split('\s+', line)
        index[words[0]] = []
        for i in range(1, len(words) - 1):
            index[words[0]].append(words[i])
    for key, value in index.items():
        index[key] = set(value)
    return index


def boolean_search(query):
    and_operator = '&'
    or_operator = '|'
    not_operator = 'not'

    index = read_index()
    all_pages = set()
    for page in index.values():
        all_pages = all_pages | page

    def and_operation(set_a, set_b):
        return set_a & set_b

    def or_operation(set_a, set_b):
        return set_a | set_b

    def difference_set(set_a, set_b):
        return set_a - set_b

    words = re.split('\s+', query)
    inversion = False

    query_in_sets = []

    prev_set = set()
    i = 0
    for i in range(len(words)):
        word = words[i]
        if i == len(words) - 1:
            prev_set = difference_set(all_pages, index[word])
            query_in_sets.append((prev_set, None))
        if word == and_operator or word == or_operator:
            query_in_sets.append((prev_set, word))
            continue

        if word == not_operator:
            inversion = True
            continue
        if inversion:
            prev_set = difference_set(all_pages, index[word])
            inversion = False
        else:
            if word not in index.keys():
                prev_set = set()
            else:
                prev_set = index[word]

    def run_operations(query, operation_symbol, operation_func):
        result = []
        for i in range(len(query) - 1):
            if query[i][1] == operation_symbol:
                current_result = operation_func(query[i][0], query[i + 1][0])
                query[i + 1] = (current_result, query[i + 1][1])
            else:
                result.append((query[i][0], query[i][1]))
        result.append((query[len(query) - 1]))
        return result

    and_result = run_operations(query_in_sets, and_operator, and_operation)
    or_result = run_operations(and_result, or_operator, or_operation)
    if len(or_result) == 1:
        print("Correct query")
    return or_result[0][0]


result = boolean_search("лионель & месси | 2010 & not год")
print(len(result))
print(result)

'''
Пример запроса для булева поиска:
"лионель & месси | 2010 & not год"

Результат
{'page16.html', 'page20.html', 'page35.html', 'page69.html', 'page47.html', 'page36.html', 'page88.html', 'page30.html', 'page114.html', 'page94.html', 'page113.html', 'page10.html', 'page119.html', 'page39.html', 'page118.html', 'page99.html', 'page91.html', 'page107.html', 'page56.html', 'page79.html', 'page49.html', 'page95.html', 'page81.html', 'page87.html', 'page58.html', 'page104.html', 'page66.html', 'page101.html', 'page22.html', 'page115.html', 'page38.html', 'page32.html', 'page42.html', 'page108.html', 'page17.html', 'page117.html', 'page5.html', 'page59.html', 'page63.html', 'page80.html'}
'''