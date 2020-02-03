# ===========================================================================
#   data.py -----------------------------------------------------------------
# ===========================================================================

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
def validate_data_tensor(data_tensor, index_list, sort=False):
    if sort:
        index_list.sort()

    for count, item_tensor in enumerate(data_tensor):
        data_tensor[count] = [data_tensor[count][i] for i in index_list ]
    return data_tensor