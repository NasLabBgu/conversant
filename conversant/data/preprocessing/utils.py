import logging
from anytree import node

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

def find_root(tree) -> int:
    """
    :parameter: tree - dictionary of {'node_id', anytree.node}

    Finds the index of the root node in a conversation tree dictionary

    """
    k = None
    for k,v in tree.items():
        if v.father == -1:
            root = k
            
    return root
            

