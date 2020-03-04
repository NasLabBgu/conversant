from anytree.exporter import DotExporter


def print_tree(root, output_name: str) -> bool:
    """
    :parameter: root: Node object of the root of the tree
    :parameter: output_name: the name of the image file generated

    prints an AnyTree object to a file jpg

    """
    DotExporter(root, nodeattrfunc=lambda root: 'label="%s %s"' % (root.author,
                                            root.name)).to_picture(output_name)

    return True