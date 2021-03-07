import random
import re
import zipfile

import requests


def open_page(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        return None


def find_inner_links(content):
    prefix = "/wiki"
    href_regex = "href=[\"\']/wiki(.*?)[\"\']"
    links = re.findall(href_regex, content)
    return list(
        map(lambda e: prefix + e, filter(lambda e: not str(e).endswith((".png", ".svg", ".jpg", ".ogg")), links)))


def create_zip_with_pages(content):
    i = 0
    with zipfile.ZipFile('reuslt.zip', 'w') as zipped_f:
        for page in content:
            zipped_f.writestr("page" + str(i) + ".html", page)
            i += 1


def create_index_txt(links):
    index_txt = open("index.txt", "w")
    pattern = "%d. %s\n"
    for i in range(len(links)):
        index_txt.write(pattern % (i, host_name + links[i]))
    index_txt.close()


if __name__ == '__main__':
    host_name = 'https://ru.wikipedia.org'
    start_url = 'https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D1%81%D1%81%D0%B8,_%D0%9B%D0%B8%D0%BE%D0%BD%D0%B5%D0%BB%D1%8C'

    max_links_number = 110

    content_start_page = open_page(start_url)
    inner_links = find_inner_links(content_start_page)

    random.shuffle(inner_links)
    inner_links = inner_links[:120]

    create_index_txt(inner_links)

    inner_links_content = []
    for link in inner_links:
        result = open_page(host_name + link)
        if result is not None:
            inner_links_content.append(result)

    create_zip_with_pages(inner_links_content)
