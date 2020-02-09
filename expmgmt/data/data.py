# ===========================================================================
#   data.py -----------------------------------------------------------------
# ===========================================================================

import re
import os

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data_tensor_intervall(data_tensor, start, end):
    return data_tensor[start:end] 

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_sub_data_tensor(data_tensor, index_list, sort=False):
    if sort:
        index_list.sort()

    for count, item_tensor in enumerate(data_tensor): 
        data_tensor[count] = [data_tensor[count][i] for i in index_list ]

    return data_tensor

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data_tensor_regex(data_tensor, regex, group):

    regex = regex if isinstance(regex, list) else [regex]
    group = group if isinstance(regex, list) else [group]

    data_tensor_dict = dict()
    for item_tensor in data_tensor: 
        item = os.path.basename(item_tensor[0])
        for r, g in zip(regex, group):
            if item:
                res = re.compile(r)
                result = res.match(item)
                item = result.group(g) if result else None
                if not item in data_tensor_dict.keys():
                    data_tensor_dict[item] = item_tensor

    return [ v for v in data_tensor_dict.values() ]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def validate_data_tensor(data_tensor, index_list, sort=False):
    return True