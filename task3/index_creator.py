import re
import zipfile
from functools import cmp_to_key

from task2.tokenization_lemmatization import tokenization, get_lemma


class WordInfo:
    def __init__(self):
        self.documents = []
        self.general_count = 0

    def append_document_info(self, document_number, document_word_count):
        self.documents.append(document_number)
        self.general_count += document_word_count


def read_lemmatization():
    f = open("../task2/lemmatization.txt", "r")
    lines = f.readlines()
    map = dict()
    for line in lines:
        key = None
        words = re.split('\s+', line)
        for i in range(len(words) - 1):
            if i == 0:
                key = words[i]
                map[key] = []
            else:
                map[key].append(words[i])
    return map


def get_document_index(filename):
    number = ""
    for letter in filename:
        if letter.isdigit():
            number += letter
    return int(number)


def sort_index(index):
    def comparator(x, y):
        return x[1].general_count - y[1].general_count

    return dict(sorted(index.items(), key=cmp_to_key(comparator), reverse=True))


def find_words_in_html_files(map):
    archive = zipfile.ZipFile('../task1/result.zip', 'r')
    index = dict()
    i = 0
    for file in archive.filelist:
        # if i == 3:
        #     break
        # i += 1
        html = archive.open(file.filename)
        html_word_list = tokenization(html)
        word_used = set()
        for word in html_word_list:
            lemma = get_lemma(word)
            if lemma in map.keys() and lemma not in word_used:
                word_used.add(lemma)
                similar_words = map[lemma]
                count = 0
                for similar_word in similar_words:
                    count += html_word_list.count(similar_word)
                if lemma not in index.keys():
                    index[lemma] = WordInfo()
                index[lemma].append_document_info(file.filename, count)
        print("end of reading doc ", file.filename)
    return dict(sorted(index.items()))


def write_index_generation_result(index):
    file = open("index.txt", "w")
    for word, doc_info in index.items():
        file_string = word + " "
        for doc in doc_info.documents:
            file_string += " " + str(doc)
        file_string += "\n"
        file.write(file_string)
    file.close()


def create_index():
    map = read_lemmatization()
    index = find_words_in_html_files(map)
    sorted_index = sort_index(index)
    write_index_generation_result(sorted_index)


def read_index():
    f = open("index.txt", "r")
    lines = f.readlines()
    map = dict()
    for line in lines:
        words = re.split('\s+', line)
        key = words[0]
        if not key in map.keys():
            map[key] = set()
        for i in range(1, len(words) - 1):
            map[key].add(words[i])
    return map


def boolean_search(query, index):
    query_words = re.split('\s+', query)
    page_crossing = set()
    token_query = set(map(lambda x: get_lemma(x), query_words))
    for word in token_query:
        page_crossing = page_crossing | index[word]
    print(page_crossing)


if __name__ == '__main__':
    create_index()
    boolean_search("лионель месси 2010 год", read_index())

'''
Пример запроса для булева поиска:
"лионель месси 2010 год"

Результат
{'page36.html', 'page117.html', 'page110.html', 'page10.html', 'page9.html', 'page85.html', 'page64.html', 'page59.html', 'page5.html', 'page105.html', 'page15.html', 'page11.html', 'page107.html', 'page40.html', 'page90.html', 'page76.html', 'page50.html', 'page82.html', 'page100.html', 'page7.html', 'page106.html', 'page53.html', 'page88.html', 'page13.html', 'page22.html', 'page81.html', 'page68.html', 'page56.html', 'page37.html', 'page34.html', 'page112.html', 'page26.html', 'page99.html', 'page52.html', 'page45.html', 'page18.html', 'page57.html', 'page73.html', 'page86.html', 'page61.html', 'page12.html', 'page0.html', 'page63.html', 'page79.html', 'page44.html', 'page55.html', 'page19.html', 'page54.html', 'page47.html', 'page69.html', 'page41.html', 'page17.html', 'page103.html', 'page96.html', 'page108.html', 'page60.html', 'page27.html', 'page104.html', 'page113.html', 'page111.html', 'page3.html', 'page35.html', 'page43.html', 'page32.html', 'page29.html', 'page24.html', 'page8.html', 'page116.html', 'page58.html', 'page91.html', 'page71.html', 'page28.html', 'page98.html', 'page97.html', 'page4.html', 'page14.html', 'page67.html', 'page84.html', 'page49.html', 'page1.html', 'page39.html', 'page114.html', 'page89.html', 'page92.html', 'page77.html', 'page93.html', 'page6.html', 'page95.html', 'page75.html', 'page30.html', 'page87.html', 'page16.html', 'page118.html', 'page119.html', 'page25.html', 'page74.html', 'page33.html', 'page80.html', 'page21.html', 'page51.html', 'page83.html', 'page101.html', 'page23.html', 'page38.html', 'page78.html', 'page70.html', 'page46.html', 'page66.html', 'page48.html', 'page94.html', 'page115.html', 'page102.html', 'page65.html', 'page109.html', 'page72.html', 'page42.html', 'page20.html'}
'''