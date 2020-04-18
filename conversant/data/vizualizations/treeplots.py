from anytree.exporter import DotExporter


def print_tree(root, print_attribute: str,  output_name: str) -> bool:
    """ Prints an AnyTree object to a file jpg
    
    Arguments:
        root {anytree.Node} -- Node of the root of the tree
        print_attribute {str} -- option to print additional feature information onto the tree
        output_name {str} -- the name of the png file to write i.e "name.png"  
    
    Returns:
        bool -- indication of the parameter 
    """
    if print_attribute is None:
        DotExporter(root, nodeattrfunc=lambda root: 'label="%s %s"' % (root.author,root.name)).to_picture(output_name)
    else:
        DotExporter(root, nodeattrfunc=lambda root: f'label="%s %s {print_attribute} %s"' % (root.author,root.name, root.__dict__[print_attribute])).to_picture(output_name)

    return True