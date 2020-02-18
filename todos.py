

# TODO A conversation is a tree of interactoons between users. interactions can be replies, likes (or upvotes), mentions etc...

# TODO load datasets from multiple sources and format
    # TODO Example dataset included in the repo (toy cmv or twitter)
    # TODO Loaders from multiple formats
        # todo load_cmv
        # todo load_twitter
        # todo ...

# TODO load functions creates a tree in multiple formats:
    # TODO load into pandas
    # TODO load into anytree.
    # TODO define what is the base data structure of a tree.
    # TODO accepts preprocessing function hook to apply during load on every tree.

# TODO preprocessing on datasets
    # TODO validate and filter trees.
    # TODO remove moderators and bots replies, and vut or re-link nodes
    # TODO standard preprocessing and custom preprocessing (interface)

# TODO structure enrichment
    # TODO interaction graphs between authors (break the tree structure)
    # TODO extract graphlets

# TODO textual enrichment
    # TODO liwc features enrichment (per post and per user)
    # TODO

# TODO Analysis
    # TODO statistics on a conversation or on multiple conversations

# TODO Embeddings
    # TODO Language model based on trees dataset
    # TODO core model - usable for multiple types of tasks.
    # TODO the core model should work on sequemce of nodes in the tree.

# TODO Visualizations

