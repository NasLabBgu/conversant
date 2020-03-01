import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def filter_under_n(all_trees) -> list:
    """:parameter
    takes a list of tree dictionaries and filter trees under N nodes
    """
    pass


def filter_over_leaf_rate(all_trees) -> list:
    """:parameter
    takes a list of tree dictionaries and filter trees that have over % of leaves.
    """
    pass


def filter_under_depth(all_trees) -> list:
    """:parameter
    takes a list of tree dictionaries and filter trees that have over % of leaves.
    """
    pass


def filter_DeltaBot(all_trees) -> list:
    """:parameter:
        takes a list of tree dictionaries and filter posts by DeltaBot and deletes his descendents.
    """
    # drop DeltaBot and his descendents
    for tree in all_trees:
        ids_to_drop = []
        for k, v in tree.items():
            if v.author == 'DeltaBot':
                ids_to_drop.append(v.index)
                ids_to_drop.append([c.index for c in v.descendants])

        tree = {key: tree[key] for key in tree if key not in ids_to_drop}
    return all_trees
