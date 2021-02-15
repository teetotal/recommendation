from cf_util import *
import argparse
from surprise import * 
from surprise import accuracy

parser = argparse.ArgumentParser()
parser.add_argument('--epochs', type=int, required=False, default=100, help="default 100.")
parser.add_argument('--model', type=str, required=False, default='similarity.cf', help="default similarity.cf.")
args = parser.parse_args()
epochs = args.epochs
model_path = args.model

trainset, aids, spids, user_item = load_train_data()
algo = load_model(model_path)
if algo == None:
    sim_options = {'name': 'pearson_baseline', 'user_based': True}
    bsl_options = {'method': 'als', 'n_epochs': epochs, 'reg_u': 10, 'reg_i': 15}
    bsl_options_sgd = {'method': 'sgd', 'n_epochs': epochs, 'learning_rate': 0.01, 'reg': 0.01}
    ##Using KNNBaseline algorithm
    algo = KNNBaseline(sim_options=sim_options, bsl_options=bsl_options)
    algo.fit(trainset)
    #dump.dump(model_path, algo=algo)
    '''
    print('Testing...')
    print('\tbuild testset')
    #accuracy
    testset = trainset.build_testset()
    print('\ttesting')
    predictions = algo.test(testset, verbose=False)
    print('\tget rmse')
    # RMSE should be low as we are biased
    rmse = accuracy.rmse(predictions, verbose=True)
    '''

algo.predict('00006b4f13ffe2bbb35aaf32', 216214100, 5, verbose=True)
algo.predict('0000170419d00fa3857e7b6d', 219226380, 5, verbose=True)