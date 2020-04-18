import datetime
import pandas as pd
import logging
from .tree_transformations import df2tree

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def load2df(path: str, input_format='csv') -> pd.DataFrame:
    """ Reads csv or json file of conversation data, the data should have at least these features
        'node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'
    
    Arguments:
        path {str} -- path to file
    
    Keyword Arguments:
        input_format {str} -- type of file (string) i.e 'csv', 'json' (default: {'csv'})
    
    Returns:
        pd.DataFrame -- requested conversation data 
    """

    if input_format == 'csv':
        df = pd.read_csv(path)
        df = df.filter(['node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'], axis=1)

        df['index1'] = df.index
        logging.info(f'Conversation sample has {df.tree_id.nunique()} unique trees')
        logging.info(f'Conversation sample has {df.author.nunique()} unique authors')
        #logging.info(f"Data is from {datetime.utcfromtimestamp(df.timestamp.min()).strftime('%Y-%m-%d')}")
        #logging.info(f"to {datetime.utcfromtimestamp(df.timestamp.max()).strftime('%Y-%m-%d')}")

    if input_format == 'pickle':
        df = pd.read_pickle(path)
        df = df.filter(['node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'], axis=1)

        df['index1'] = df.index
        logging.info(f'Conversation sample has {df.tree_id.nunique()} unique trees')
        logging.info(f'Conversation sample has {df.author.nunique()} unique authors')
        #logging.info(f"Data is from {datetime.utcfromtimestamp(df.timestamp.min()).strftime('%Y-%m-%d')}")
        #logging.info(f"to {datetime.utcfromtimestamp(df.timestamp.max()).strftime('%Y-%m-%d')}")

    if input_format == 'json':
        # TODO: add code for reading json to df RON
        df = None

    return df


def load2anytree(path: str, input_format='csv') -> list:
    """ Reads csv or json file of conversation data, the data should have at least these features
        'node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'
    
    Arguments:
        path {str} -- path to file 
    
    Keyword Arguments:
        input_format {str} -- [description] (default: {'csv'})
    
    Returns:
        list -- list of dictionaries with post id as keys and anytree.Node objects as values.
    """

    if input_format == 'csv':
        df = pd.read_csv(path)
        df = df.filter(['node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'], axis=1)

        df['index1'] = df.index
        logging.info(f'Conversation sample has {df.tree_id.nunique()} unique trees')
        logging.info(f'Conversation sample has {df.author.nunique()} unique authors')
        logging.info(f"Data is from {datetime.utcfromtimestamp(df.timestamp.min()).strftime('%Y-%m-%d')}")
        logging.info(f"to {datetime.utcfromtimestamp(df.timestamp.max()).strftime('%Y-%m-%d')}")

    if input_format == 'pickle':
        df = pd.read_pickle(path)
        df = df.filter(['node_id', 'tree_id', 'timestamp', 'author', 'text', 'parent'], axis=1)
        df['index1'] = df.index
        logging.info(f'Conversation sample has {df.tree_id.nunique()} unique trees')
        logging.info(f'Conversation sample has {df.author.nunique()} unique authors')

    if input_format == 'json':
        # TODO: add code for reading json to df RON
        df = None

    trees_l = list(df.tree_id)
    grouped = df[df.tree_id.isin(trees_l)].groupby('tree_id')
    all_trees = [df2tree(group) for name, group in grouped]
    logging.info(f'Done converting {len(all_trees)} conversations to trees')

    return all_trees


