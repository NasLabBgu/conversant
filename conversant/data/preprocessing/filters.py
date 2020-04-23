import logging
from anytree.search import findall
from .utils import find_root

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def filter_under_n(all_trees: list, n: int) -> list:
    """ Takes a list of tree dictionaries and filter trees that have under n nodes. 
    
    Arguments:
        all_trees {list} -- list of dictionary conversation trees like [{'node_id: node object}]
        n {int} -- the minimum number of nodes accepted in the tree
    
    Returns:
        list -- list of dictionary conversation trees like [{'node_id: node object}] after processing 
    """

    all_trees_processed = []
    
    logging.info(f'filtering trees under {n} nodes, input count of trees is {len(all_trees)}')
    for tree in all_trees:
        if len(tree) >= n:
            all_trees_processed.append(tree)
        else:
            pass
    logging.info(f'filtered, output count of trees is {len(all_trees_processed)}')

    return all_trees_processed


def filter_over_leaf_rate(all_trees) -> list:
    pass


def filter_under_depth(all_trees: list, depth: int) -> list:
    """ Takes a list of tree dictionaries and filter trees that are under the given depth.
    
    Arguments:
        all_trees {list} -- list of dictionary conversation trees like [{'node_id: node object}]
        depth {int} -- the minimum depth of a tree to be included in the dataset 
    
    Returns:
        list -- list of dictionary conversation trees like [{'node_id: node object}] after processing 
    """

    all_trees_processed = []
    
    logging.info(f'filtering trees under {depth+1}, input count of trees is {len(all_trees)}')
    for tree in all_trees:
        root = find_root(tree)
        if findall(tree[root], filter_=lambda node: node.depth > 2):
            all_trees_processed.append(tree)
        else:
            pass
    logging.info(f'filtered, output count of trees is {len(all_trees_processed)}')

    return all_trees_processed


def filter_DeltaBot(all_trees: list) -> list:
    """ Takes a list of tree dictionaries and filter posts by 'DeltaBot' and deletes his descendents.
    
    Arguments:
        all_trees {[type]} -- list of dictionary conversation trees like [{'node_id: node object}]
    
    Returns:
        list -- list of dictionary conversation trees like [{'node_id: node object}] after processing 
    """

    # drop DeltaBot and his descendents
    for tree in all_trees:
        ids_to_drop = []
        for k, v in tree.items():
            if v.author == 'DeltaBot':
                ids_to_drop.append(v.index)
                ids_to_drop.append([c.index for c in v.descendants])

        tree = {key: tree[key] for key in tree if key not in ids_to_drop}
    logging.info('conversations are now free of DeltaBot and his descendents')
    
    return all_trees
