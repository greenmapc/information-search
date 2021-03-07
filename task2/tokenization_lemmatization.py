import string
import zipfile

import nltk
import pymorphy2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


def tokenization(html):
    soup = BeautifulSoup(html).get_text()
    tokenization_condition = get_tokenization_condition()
    result = set((filter(tokenization_condition, nltk.wordpunct_tokenize(soup))))
    result = exclude_punctuation(result)
    result = set(filter(exclude_trash(), result))
    return result


def exclude_trash():
    trash = ['«', '»', '→', '·', '®', '▼', '–', '▸', 'x', 'X']
    return lambda word: word not in trash


def exclude_punctuation(values):
    return [i for i in values if all(not j in string.punctuation for j in i)]


def get_tokenization_condition():
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на', 'o'])
    return lambda word: word not in stop_words


def write_tokenization_result(result):
    index_txt = open("tokenization.txt", "w")
    pattern = "%s\n"
    for word in result:
        index_txt.write(pattern % word)
    index_txt.close()


def lemmatization(tokenization_result):
    morph = pymorphy2.MorphAnalyzer()
    lemmatization_map = dict()
    for word in tokenization_result:
        p = morph.parse(word)[0]
        if p.normalized.is_known:
            normal_form = p.normal_form
        else:
            normal_form = word.lower()
        if not normal_form in lemmatization_map:
            lemmatization_map[normal_form] = []
        lemmatization_map[normal_form].append(word)
    return lemmatization_map


def write_lemmatization_result(lemmatization_result):
    file = open("lemmatization.txt", "w")
    for lemma, tokens in lemmatization_result.items():
        file_string = lemma + " "
        for token in tokens:
            file_string += token + " "
        file_string += "\n"
        file.write(file_string)
    file.close()


def read_file(archive, file_name):
    html = archive.open(file_name)
    return html


if __name__ == '__main__':
    nltk.download('stopwords')
    archive = zipfile.ZipFile('../task1/result.zip', 'r')
    tokenization_result = set()
    for file in archive.filelist:
        current_html_file = read_file(archive, file.filename)
        current_file_tokenization_result = tokenization(current_html_file)
        tokenization_result = tokenization_result | current_file_tokenization_result
        print("tokenization for", file.filename, "finished")
    write_tokenization_result(tokenization_result)
    lemmatization_result = lemmatization(tokenization_result)
    write_lemmatization_result(lemmatization_result)
