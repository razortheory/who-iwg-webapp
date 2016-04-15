def markdown_ordered_dict_prepend(dct, key, value):
    """inserting element to the top of markdown.odict.OrderedDict
    Args:
        dct (markdown.odict.OrderedDict): ordered dict.
        key: key to insert into dict.
        value: value to prepend.
    """

    dct[key] = value
    dct.keyOrder.remove(key)
    dct.keyOrder.insert(0, key)
