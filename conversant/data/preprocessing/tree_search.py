import logging
from anytree import node

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def find_root(tree: dict) -> int:
    """ Finds the index of the root node in a conversation tree dictionary
    
    Arguments:
        tree {dict} -- dictionary of {'node_id', anytree.node}
    
    Returns:
        int -- index of the root of the tree 
    """

    k = None
    for k,v in tree.items():
        if v.father == -1:
            root = k
            
    return root
            

