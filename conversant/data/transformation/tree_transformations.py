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
        tree = {x.post_index: Node(name=x.node_id, tree_id=x.tree_id, post_index=x.post_index, timestamp=x.timestamp,
                               author=x.author, text=x.text, father=x.parent, clean_text=x.clean_text) for i, x in
                df.iterrows()}
    else:
        # create Node objects for all instances in the df
        tree = {x.post_index: Node(name=x.node_id, tree_id=x.tree_id, post_index=x.post_index, timestamp=x.timestamp,
                               author=x.author, text=x.text, father=x.parent) for i, x in df.iterrows()}
    # update parents
    for _, v in tree.items():
        v.parent = None if v.father == -1 else tree[v.father]

    # drop DeltaBot and his descendents
    ids_to_drop = []
    for _, v in tree.items():
        if v.author == 'DeltaBot':
            ids_to_drop.append(v.post_index)
            ids_to_drop.append([c.post_index for c in v.descendants])

    final_tree = {key: tree[key] for key in tree if key not in ids_to_drop}

    return final_tree

def tree2df(tree: dict, features: dict) -> pd.DataFrame:
    """ transforms a tree dictionary structure to a pandas dataframe
    
    Arguments:
        tree {dict} -- conversation data in tree dictionary form 
        features {dict} <optional> -- dictionary containing node features like {'feature_name': function}
    
    Returns:
        pd.DataFrame -- pandas dataframe representation of the conversation tree
    """

    base_features = {'post_index':  None, 'name': None, 'tree_id': None, 
                    'timestamp': None, 'author': None, 'text': None,
                    'father': None, 'label': None}

    features.update(base_features)

    tree_features = [{feature: v.__dict__[feature] for feature in features.keys()}
                                        for _,v in tree.items()]

    df = pd.DataFrame.from_records(tree_features)
    df.index = df.post_index

    return df




    
