import re
import zipfile
from functools import cmp_to_key

from task2.tokenization_lemmatization import tokenization, get_lemma


def read_tokens():
    f = open("../task2/lemmatization.txt", "r")
    lines = f.readlines()
    tokens = set()
    for line in lines:
        words = re.split('\s+', line)
        tokens.add(words[0])
    return tokens


def read_index():
    f = open("../task3/index.txt", "r")
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


def read_tf():
    f = open("tf.txt", "r")
    lines = f.readlines()
    tf_map = dict()
    for line in lines:
        words = re.split('\s+', line)
        key = words[0]
        for i in range(1, len(words) - 2, 2):
            if key not in tf_map:
                tf_map[key] = []
            tf_map[key].append((words[i], words[i + 1]))
    return tf_map


def read_idf():
    f = open("idf.txt", "r")
    lines = f.readlines()
    idf_map = dict()
    for line in lines:
        words = re.split('\s+', line)
        idf_map[words[0]] = words[1]
    return idf_map


def write_tf(tf_map):
    file = open("tf.txt", "w")
    for word, tf_list in tf_map.items():
        file_string = word + " "
        for tf in tf_list:
            file_string += " " + tf[0] + " " + str(tf[1])
        file_string += "\n"
        file.write(file_string)
    file.close()


def write_idf(idf_map):
    file = open("idf.txt", "w")
    for word, idf in idf_map.items():
        file_string = word + " " + str(idf)
        file_string += "\n"
        file.write(file_string)
    file.close()


def write_tf_idf(tf_idf_map):
    file = open("tf_idf.txt", "w")
    for word, tf_list in tf_idf_map.items():
        file_string = word + " "
        for tf in tf_list:
            file_string += " " + tf[0] + " " + str(tf[1])
        file_string += "\n"
        file.write(file_string)
    file.close()

def tf_calculate():
    archive = zipfile.ZipFile('../task1/result.zip', 'r')
    tf_map = dict()
    for file in archive.filelist:
        tf_page_map = dict()
        html = archive.open(file.filename)
        html_word_list = tokenization(html)
        for word in html_word_list:
            lemma = get_lemma(word)
            if lemma in tf_page_map.keys():
                tf_page_map[lemma] += 1
            else:
                tf_page_map[lemma] = 1
        for key, value in tf_page_map.items():
            if key not in tf_map.keys():
                tf_map[key] = []
            tf = round(value / len(html_word_list), 3)
            if tf != 0:
                tf_map[key].append((file.filename, round(value / len(html_word_list), 3)))
        print("read tf for", file.filename)
    return tf_map


def idf_calculate():
    archive = zipfile.ZipFile('../task1/result.zip', 'r')
    documents_number = len(archive.filelist)
    token_document_map = dict()
    index = read_index()
    for element, pages in index.items():
        token_document_map[element] = round(len(pages) / documents_number, 3)
    return token_document_map


def tf_idf_calculate():
    def comparator(x, y):
        return y[1] - x[1]
    def map_comparator(x, y):
        return len(x[1]) - len(y[1])

    tf_data = dict(sorted(read_tf().items()))
    idf_data = dict(sorted(read_idf().items()))
    tf_idf_map = dict()
    for token, documents_tf in tf_data.items():
        tf_idf_map[token] = []
        for document_tf in documents_tf:
            document = document_tf[0]
            tf = float(document_tf[1])
            tf_idf_map[token].append((document, tf * float(idf_data[token])))
    for key, value in tf_idf_map.items():
        tf_idf_map[key] = sorted(value, key=cmp_to_key(comparator))
    return dict(sorted(tf_idf_map.items(), key=cmp_to_key(map_comparator), reverse=True))


# tf_result = tf_calculate()
# write_tf(tf_result)
tf_idf_result = tf_idf_calculate()
write_tf_idf(tf_idf_result)
# idf_result = idf_calculate()
# write_idf(idf_result)
