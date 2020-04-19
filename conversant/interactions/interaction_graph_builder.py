

def parse_users_interactions(tree: Node, anonymous: bool = False) -> Dict[str, Dict[str, UsersInteraction]]:
    """
    parse the different interactions of the users in the given conversation 'tree' between the users.
    :param anonymous:
    :param tree: conversation tree
    :return: interactions graph between the users in the tree, such that each edge in the graph
             represents a summary of multiple types of interactions between the two adjacent users.
    """
    # get OP and the first node of the conversation and initialize variables
    first_node = tree.node
    if anonymous:
        first_node[AUTHOR_FIELD] = "user0"

    op: str = first_node[AUTHOR_FIELD]
    interactions: Dict[str, Dict[str, UsersInteraction]] = {op: {}}
    current_branch_nodes: List[dict] = [first_node]     # Stores the previous nodes in the parsed branch

    users_index = {}
    if anonymous:
        user_index = users_index.setdefault(op, len(users_index))
        op = f"user{user_index}"

    tree_nodes = walk_tree(tree)
    next(tree_nodes)    # skip the first node
    for depth, node in tree_nodes:
        # check if the entire current branch was parsed, and start walking to the next branch
        if depth < len(current_branch_nodes):
            del current_branch_nodes[depth:]

        text = node[TEXT_FIELD]
        timestamp = 0 # node[TIMESTAMP_FIELD]
        current_author = node[AUTHOR_FIELD]
        if anonymous:
            user_index = users_index.setdefault(current_author, len(users_index))
            current_author = f"user{user_index}"
            node[AUTHOR_FIELD] = current_author

        author_interactions = interactions.setdefault(current_author, {})

        # Check if deltabot awarded a delta
        delta_users = get_delta_users(current_author, text, op, current_branch_nodes)
        if delta_users is not None:
            delta_giver, delta_recipient = delta_users
            giver_interactions = interactions.setdefault(delta_giver, {})
            pair_interactions = giver_interactions.setdefault(delta_recipient, UsersInteraction())
            pair_interactions.num_confirmed_delta_awards += 1
        elif current_author == DELTA_BOT_USER:
            pass
        else:
            # parse current node interactions and add to interactions graphs
            prev_author = current_branch_nodes[-1][AUTHOR_FIELD]
            add_reply_interactions(prev_author, author_interactions)
            add_mentions_interactions(text, author_interactions)
            add_quotes_interactions(text, tree, current_branch_nodes, timestamp, author_interactions)
            add_labels(node, prev_author, author_interactions)

        current_branch_nodes.append(node)

    if DELTA_BOT_USER in interactions:
        del interactions[DELTA_BOT_USER]

    return interactions