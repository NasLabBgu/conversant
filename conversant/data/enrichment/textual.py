import pandas as pd
import logging
from .text_enrichment import clean_text, remove_punctuation
from anytree import Node
import tqdm

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def clean_text_field(data):
   """ Enriches a dataframe or Anytree structure containing "text" field with "clean text" field
      See utils.clean_text for more information
   
   Returns:
      [pd.DataFrame or dictionary] -- conversations with new clean text field 
   """

   if isinstance(data, pd.DataFrame):
      c_text = data.text.apply(lambda x: clean_text(x))
      data = data.assign(clean_text=c_text)

   if isinstance(data, list):
      for tree in tqdm.tqdm(data):
         for _,v in tree.items():
               v.clean_text = clean_text(v.text)
               
   logging.info('Added new clean text feature')
   return data

def remove_punctuation_from_text(data):
   """ Enriches a dataframe or Anytree structure containing "text" field with "clean text" field
   See utils.clean_text for more information

   Returns:
   [pd.DataFrame or dictionary] -- conversations with new clean text field 
   """

   if isinstance(data, pd.DataFrame):
      raise NotImplementedError

   if isinstance(data, list):
      for tree in tqdm.tqdm(data):
         for _,v in tree.items():
               v.text = remove_punctuation(v.text)
            
   logging.info('Removed punctuation from text')
   return data
