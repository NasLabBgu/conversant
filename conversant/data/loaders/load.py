import datetime
import pandas as pd
import logging
from .utils import df2tree

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def load2df(path, input_format='csv') -> pd.DataFrame:
    """
    :parameter path: path to file
    :parameter input_format: type of file (string) i.e 'csv', 'json'
    :returns: pandas data frame

    Reads csv or json file of conversation data, the data should have at least these features
    'node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'

    TODOs:
        1. support reading multiple files from a folder
        2. support reading of json file
    """
    if input_format == 'csv':
        df = pd.read_csv(path)
        df = df.filter(['node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'], axis=1)

        df['index1'] = df.index
        logging.info(f'Conversation sample has {df.tree_id.nunique()} unique trees')
        logging.info(f'Conversation sample has {df.author.nunique()} unique authors')
        logging.info(f"Data is from {datetime.utcfromtimestamp(df.timestamp.min()).strftime('%Y-%m-%d')}")
        logging.info(f"to {datetime.utcfromtimestamp(df.timestamp.max()).strftime('%Y-%m-%d')}")

    if input_format == 'json':
        # TODO: add code for reading json to df RON
        df = None

    return df


def load2anytree(path, input_format='csv') -> pd.DataFrame:
    """
    :parameter path: path to file
    :parameter input_format: type of file (string) i.e 'csv', 'json'
    :returns: dictionary with post id as keys and Anytree.Node objects as values.

    Reads csv or json file of conversation data, the data should have at least these features
    'node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'

    TODOs:
        1. support reading multiple files from a folder
        2. support reading of json file
    """
    if input_format == 'csv':
        df = pd.read_csv(path)
        df = df.filter(['node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'], axis=1)

        df['index1'] = df.index
        logging.info(f'Conversation sample has {df.tree_id.nunique()} unique trees')
        logging.info(f'Conversation sample has {df.author.nunique()} unique authors')
        logging.info(f"Data is from {datetime.utcfromtimestamp(df.timestamp.min()).strftime('%Y-%m-%d')}")
        logging.info(f"to {datetime.utcfromtimestamp(df.timestamp.max()).strftime('%Y-%m-%d')}")

    if input_format == 'json':
        # TODO: add code for reading json to df RON
        df = None

    trees_l = list(df.tree_id)
    grouped = df[df.tree_id.isin(trees_l)].groupby('tree_id')
    all_trees = [df2tree(group) for name, group in grouped]
    logging.info(f'done converting {len(all_trees)} conversations to trees')

    return all_trees


