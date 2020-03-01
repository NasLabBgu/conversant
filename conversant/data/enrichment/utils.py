import re
import logging
import tldextract
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def clean_text(text):
    if type(text) is not str:
        text = ''
    if text == '[deleted]' or text == '[removed]':
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