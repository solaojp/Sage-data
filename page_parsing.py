#science Direct Page save as HTML only
"""
1) 75 Records in CSv
2) Image folder
3) Table folder
4) Highlights / abstract
5) Image to Text Extraction
6) Table to Text
7) from PDF

"""
from bs4 import BeautifulSoup
import urllib.request
import os
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import csv


# Parsing the title
def _get_title(soup,row):
    title = soup.find_all('title')
    row.update({'Titles':title[0].string})
    #print(title[0].string)


# Parsing the authors
def _authors_parsing(soup,row):
    # TODO: add Authors to CSV
    list = []
    authors = soup.find_all('span')
    #print(authors)
    for span_tag in authors:
        #print(type(span_tag))
        attributes = span_tag.attrs
        #print(attributes)
        if 'class' in attributes:
            #print(attributes)
            class_list = attributes['class']
            #print(class_list)
            if 'given-name' in class_list:
                list.append(span_tag.string)
                #print(span_tag.string)
            elif 'surname' in class_list:
                list.append(span_tag.string)
                #print(span_tag.string)
    row.update({'Authors':list})

# Parsing the keywords
def _keywords_parsing(soup,row):
    list = []
    keywords = soup.find_all('div')     #returns list object
    for div_tag in keywords:
        attributes = div_tag.attrs     #returns dict object
        if "class" in attributes:
            class_list = attributes['class']
            if "keyword" in class_list:
                list.append(div_tag.string)
                #print(div_tag.string)
    row.update({'Keywords':list})

#HTMLFiles/Epileptic spasms as the presenting seizure type in a patient with a new ?O? of TORCH, congenital Zika virus infection - ScienceDirect.html
def _abstract_highlights_parsing(soup,row):
    _abstract = ''
    highlights = soup.find("div",{"class":"Abstracts u-font-serif"},{'id':"abstracts"})
    #print(type(highlights))
    for_parsing = str(highlights)
    para = BeautifulSoup(for_parsing,'html.parser').find_all('p')
    for p in para:
        #print(p.string)
        _abstract += str(p.string)
    row.update({'Abstract/Highlights': _abstract})
    _wordcloud_abstract(_abstract)
    # # TODO: Create the frequency shit >>

def _wordcloud_abstract(text):
    if len(text)==0:
        return
    global count
    filename = 'wordcloud'+str(count)+'.png';
    count += 1
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(background_color="black", max_words=2000,
                   stopwords=stopwords, contour_width=3, contour_color='steelblue').generate(text).to_file(filename)

# Parsing the images
def _image_parsing(soup,row):
    list = []
    images = soup.find_all('img')
    for img_tag in images:
        list.append(img_tag.get('src'))
        _store(img_tag.get('src'))
        #print(img_tag.get('src'))
    row.update({'Images':list})

def _store(path):
    url = path
    filename = url[url.rfind("/")+1:]
    if not os.path.exists('Images'):
        # Create target Directory
        os.mkdir('Images')
    try:
        urllib.request.urlretrieve(url, 'Images/'+filename)
    except Exception as e:
        print(e)



# Preparing a BeautifulSoup object for parsing
def _get_soup(path):
    page = open(path,'r')
    page = page.read()
    soup = BeautifulSoup(page,'html.parser')
    return soup

if __name__ == '__main__':
    #Global count for wordcloud files
    count = 0;
    #path = 'Paclitaxel eluting balloon plus spot bare metal stenting for diffuse and very long coronary disease. (PEB-long pilot study) - ScienceDirect.html'
    # CSV File - Read
    df = pd.read_csv('Gajanan_Maharaj_Prasanna.csv', index_col=0)
    #  ,header=None ,skiprows=1 , names=['Cal', 'Pr', 'Fat', 'sod', 'Fib', 'Rting']
    field_names = ['Titles', 'Authors', 'Keywords', 'Abstract/Highlights', 'Images']
    with open('text_mining.csv', 'a', newline='') as csvfile:
        fieldnames = ['This','aNew']
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        # writer.writerow({'latitude':'is', 'date':'Row'})
        # writer.writerow({'latitude':'is', 'user':'Row', 'text':'Row'})
        for line in df.iterrows():
            #print(line[0])
            path = 'HTMLFiles/'+line[0]
            print('>>>>>>>')
            data = {}
            soup = _get_soup(path)
            _get_title(soup,data)   #title
            _authors_parsing(soup,data)   #authors
            _keywords_parsing(soup,data)   #Keywords
            _abstract_highlights_parsing(soup,data) #highlights
            _image_parsing(soup,data)    #images
            writer.writerow(data)

            print(data)
