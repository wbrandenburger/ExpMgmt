# ===========================================================================
#   dictionary.py -----------------------------------------------------------
# ===========================================================================

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def update_dict(a, b):
    # @todo[comment]:
    if a and b and isinstance(a, dict):
        a.update(b)
    return a

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_dict_element(dict_list, field, query):
    # @todo[comment]:
    for item in dict_list:
        if item[field] == query:
            return item
    return dict()

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_dict_elements(dict_list, field, query, update=False):
    # @todo[comment]:
    if not isinstance(field, list) and isinstance(query, list): 
        field = [field] * len(query)

    result = list() if not update else dict()
    if isinstance(field, list) and isinstance(query, list):
        for field_item, query_item in zip(field, query):
            item = get_dict_element(dict_list, field_item, query_item)
            if item:
                if not update:
                    result.append(item)
                else:
                    result.update(item)

    return result

