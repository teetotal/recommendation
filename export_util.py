from sql import *
from hyper_params import *
########################################################
s = sql(get_hyperparams())
####################################################################
def get_query(sql_file_path):
    with open(sql_file_path, 'r') as file:
        q = file.read()
    return q
def get_data(query):
    return s.get_rows(query)
