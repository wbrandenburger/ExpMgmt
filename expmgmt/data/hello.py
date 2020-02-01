# ===========================================================================
#   data.py -----------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import os
import re

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def get_files_of_folder(path):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def get_file_pattern_of_folder(path, pattern):
    regex_pattern = re.compile(pattern)

    return [regex_pattern.match(f).group(1) for f in get_files_of_folder(path)]

#   function ----------------------------------------------------------------
# ---------------------------------------------------------------------------
def set_trainings_data(path_list: list, pattern_list:list):
    """First entry of trainings_data is reference"""

    
    return path