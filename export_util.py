from sql import *
from hyper_params import *
########################################################
s = sql(get_hyperparams())
####################################################################
def get_data(query):
    return s.get_rows(query)
def insert(query):
    s.execute(query)
