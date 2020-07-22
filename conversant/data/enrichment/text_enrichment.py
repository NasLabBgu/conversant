import re
import os
import logging
import string
import tldextract
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def clean_text(text) -> str:
    """ Preprocesses text into a clean version
    
    Arguments:
        text {str} -- input free text
    
    Returns:
        str -- preprocessed clean text
    """

    if type(text) is not str:
        text = str(text)
    if text == '[deleted]':
        text = '' 
    if text == '[removed]':
        text = ''
    deltabot_re = re.compile(r'^Confirmed: \d+ delta awarded to .*', re.DOTALL)
    if deltabot_re.match(text):
        text = ''
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    mentions_re = re.compile(r'/u/\w*', re.MULTILINE)
    quote_re = re.compile(r'<quote>.[^<]*</quote>', re.MULTILINE)
    url_re = re.compile(r'http://[^\s]*', re.MULTILINE)
    for m in mentions_re.findall(text):
        text = text.replace(m, '_mention_')
    for q in quote_re.findall(text):
        text = text.replace(q, '_quote_')
    for url in url_re.findall(text):
        text = '_url_' + text.replace(url, tldextract.extract(url).domain)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    return text


def load_liwc():
    fin = open('./LIWC_Features.txt')
    lines = fin.readlines()
    fin.close()

    liwc_cat_dict = {}  # {cat: (w1,w2,w3,...)}

    for line in lines[1:]:  # first line is a comment about the use of *
        tokens = line.strip().lower().split(', ')
        liwc_cat_dict[tokens[0]] = tokens[1:]

    return liwc_cat_dict


def remove_punctuation(text:str) -> str:
    exclude = set(string.punctuation)
    return  ''.join(ch for ch in text if ch not in exclude)
