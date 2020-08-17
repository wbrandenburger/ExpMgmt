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
def get_data_tensor_regex(data_tensor, regex, group, folder=False, number=None):

    regex = regex if isinstance(regex, list) else [regex]
    group = group if isinstance(regex, list) else [group]

    data_tensor_dict = list()
    data_tensor_list = list()
    num = 1
    for item_tensor in data_tensor:

        item = item_tensor[0]
        if not folder:
            item = os.path.basename(item_tensor[0])
            
        for r, g in zip(regex, group):
            if item:
                res = re.compile(r)
                result = res.match(item)
                item = result.group(g) if result else None
                if not item in data_tensor_dict:
                    num = 1
                    data_tensor_dict.append(item)
                    data_tensor_list.append(item_tensor)
                elif number is not None and num < number:
                    num += 1
                    data_tensor_list.append(item_tensor)
                    
    return  data_tensor_list
    
#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data_tensor_indices(data_tensor, index_list):
    new_data_tensor = [None]*len(index_list) 
    for count, item in enumerate(index_list): 
        new_data_tensor[count] = data_tensor[item]

    return new_data_tensor

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_data_tensor_not_none(data_tensor):
    import pathlib

    new_data_tensor = list()
    for item in data_tensor:
        append= True
        for path in item:
            if not path or not pathlib.Path(path).is_file():
                append = False
        if append:
            new_data_tensor.append(item)
    return new_data_tensor

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def validate_data_tensor(data_tensor, index_list, sort=False):
    return True