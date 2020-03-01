import re
import logging
import tldextract
from .utils import clean_text
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def clean_text_field(df):
    clean_text = df.text.apply(clean_text)
    df = df.assign(clean_text=clean_text)
    return df

