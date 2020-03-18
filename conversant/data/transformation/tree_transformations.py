from anytree import Node
import pandas as pd
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def df2tree(df: pd.DataFrame) -> dict:
    """ Transforms a pandas dataframe with tree information and converts to tree data type
    
    Arguments:
        df {pd.DataFrame} -- conversation dataframe
    
    Returns:
        dict -- dictionary like {'node_id': anytree.node}
    """

    if 'clean_text' in df.columns:
        # create Node objects for all instances in the df
        tree = {x.index1: Node(name=x.node_id, tree_id=x.tree_id, index=x.index1, timestamp=x.timestamp,
                               author=x.author, text=x.text, father=x.parent, clean_text=x.clean_text) for i, x in
                df.iterrows()}
    else:
        # create Node objects for all instances in the df
        tree = {x.index1: Node(name=x.node_id, tree_id=x.tree_id, index=x.index1, timestamp=x.timestamp,
                               author=x.author, text=x.text, father=x.parent) for i, x in df.iterrows()}
    # update parents
    for _, v in tree.items():
        v.parent = None if v.father == -1 else tree[v.father]

    # drop DeltaBot and his descendents
    ids_to_drop = []
    for k, v in tree.items():
        if v.author == 'DeltaBot':
            ids_to_drop.append(v.index)
            ids_to_drop.append([c.index for c in v.descendants])

    final_tree = {key: tree[key] for key in tree if key not in ids_to_drop}

    return final_tree

def tree2df(tree: dict, features: list) -> pd.DataFrame:
    """ transforms a tree dictionary structure to a pandas dataframe
    
    Arguments:
        tree {dict} -- [description]
        features {list} -- [description]
    
    Returns:
        pd.DataFrame -- [description]
    """
    tree_features = {feature: v.__dict__[feature] for feature in features
                                     for k,v in tree.items()}

    columns=['index1', 'node_id', 'tree_id', 'timestamp',
     'author', 'text', 'clean_text', 'parent'] + features

    df = pd.DataFrame(tree_features, columns)
    df.index = df.index1

    return df




    
