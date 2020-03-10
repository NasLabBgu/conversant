from anytree.exporter import DotExporter


#TODO: how can I inject the attibute goten as string to a value? 
def print_tree(root, print_attribute: str,  output_name: str) -> bool:
    """
    :parameter: root: Node object of the root of the tree
    :parameter: output_name: the name of the image file generated

    prints an AnyTree object to a file jpg

    """
    if print_attribute is None:
        DotExporter(root, nodeattrfunc=lambda root: 'label="%s %s"' % (root.author,root.name)).to_picture(output_name)
    else:
        DotExporter(root, nodeattrfunc=lambda root: 'label="%s %s %s"' % (root.author,root.name)).to_picture(output_name)

    return True