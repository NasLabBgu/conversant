import pandas as pd
import logging
from .utils import clean_text
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def clean_text_field(df) -> pd.DataFrame:
    """:parameter: df containing a field called "text"
       :returns: df with additional field called "clean_text"

       Enriches a dataframe containing "text" field with "clean text" field
       See utils.clean_text for more information

    """
    c_text = df.text.apply(lambda x: clean_text(x))
    df = df.assign(clean_text=c_text)
    return df



# how to log into git?
# how to define interpeter?