import urllib2
from nytimesarticle import articleAPI
from bs4 import BeautifulSoup
import os
import time
import re

TXT_EXTENSION = '.txt'

WEBDATA_RELATIVE_PREFIX = 'data/webdata/url_'

URLS_RELATIVE_PATH = 'data/urls.txt'

API_KEY = 'ffd404f8bd874e2b881367f933dd423b'


def get_data_from_url(url):
    f = urllib2.urlopen(url)
    return f.read()


def generate_input_files(from_file_no=1, to_file_no=300):
    urls_file_path = get_file_path(URLS_RELATIVE_PATH)
    if os.path.exists(urls_file_path):
        file_no = 1
        with open(urls_file_path) as urls_file:
            for url in urls_file:
                if file_no > to_file_no:
                    break
                if file_no < from_file_no:
                    file_no += 1
                    continue
                else:
                    print str(file_no)
                    print 'Getting content of: ' + str(url)
                    html_content = get_data_from_url(url)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    create_file_path = get_file_path(WEBDATA_RELATIVE_PREFIX + str(file_no) + TXT_EXTENSION)
                    if not os.path.exists(create_file_path):
                        with open(create_file_path, 'w') as to_write_file:
                            find_all = get_paras(soup, url)
                            # print find_all
                            for para in find_all:
                                to_write_file.write(para.get_text().encode('utf8'))
                                to_write_file.write('\n')
                    else:
                        print create_file_path + ' exists. Not overriding and terminating. [FATAL]'
                        break
                    file_no += 1
    else:
        print urls_file_path + ' not found. Please generate urls first. [FATAL]'
        # html_content = get_data_from_url(
        #     'https://www.nytimes.com/2018/02/18/us/politics/russian-operatives-facebook-twitter.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=a-lede-package-region&region=top-news&WT.nav=top-news')


def generate_url_file(start_page_number=0, to_extract=400):
    urls_file_path = get_file_path('data/urls.txt')
    if not os.path.exists(urls_file_path):
        with open(urls_file_path, 'w') as to_write_file:
            count = 0
            page_number = start_page_number
            previous_count = count
            while count < to_extract:
                previous_count = count
                # https: // api.nytimes.com / svc / search / v2 / articlesearch.json?api - key = ffd404f8bd874e2b881367f933dd423b & fq = news_desk:(
                # "Politics")
                # AND
                # type_of_material:("News") & page = 0 & fl = web_url
                ny_api = articleAPI(API_KEY)
                filters = {
                    'news_desk': 'Politics',
                    'type_of_material': 'News',
                }
                # news_desk_fltr = urllib.quote('&fq=news_desk:(Politics)')
                # section_fltr = 'AND section_name:("Business")'
                # source_fltr = 'AND source:("The New York Times")'
                # material_type_fltr = urllib.quote('AND type_of_material:(News)')
                # page_number_fltr = urllib.quote('&page=' + str(page_number))
                # projection = urllib.quote('&fl=web_url')
                # ny_times_url = base_url + news_desk_fltr + material_type_fltr + page_number_fltr + projection
                # json_content = json.load(urllib2.urlopen(ny_times_url))
                json_content = ny_api.search(fq=filters, page=page_number)
                num_hits = json_content[u'response'][u'meta'][u'hits']
                print 'Number of hits is: ' + str(num_hits) + '. Current count is: ' + str(count)
                if num_hits < to_extract:
                    print 'Number of hits is less than to extract. Resizing. [WARNING]!!'
                    to_extract = num_hits
                results = json_content[u'response'][u'docs']
                for result in results:
                    url = result[u'web_url']
                    to_write_file.write(url)
                    to_write_file.write('\n')
                    count = count + 1
                page_number += 1
                time.sleep(1)
                if previous_count == count:
                    print 'no more result'
                    break

    else:
        print urls_file_path + ' already exists. Not Over writing [INFO]'


def test_url(url):
    html_content = get_data_from_url(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    print soup.prettify()
    find_all = get_paras(soup, url)
    print find_all


def get_paras(soup, url):
    find_all = soup.find_all('p', class_='story-body-text story-content')
    if len(find_all) == 0:
        find_all = soup.find_all('p', class_=re.compile("^Paragraph-"))
    if len(find_all) == 0:
        find_all = soup.find_all('div', class_="articleBody")
    if len(find_all) == 0:
        print 'No content found for: ' + url
    return find_all


def get_file_path(file_name):
    current_file_path = os.path.dirname(__file__)
    return os.path.join(current_file_path, '../../' + file_name)
