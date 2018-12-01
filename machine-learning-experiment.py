import get_team_features
import get_wr_features
import get_cb_features

from sklearn.decomposition import PCA
import _pickle as pickle
import numpy as np
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, SGDClassifier
import operator, csv
from sklearn.preprocessing import StandardScaler

def select_repl(l, n):
    indices = np.random.randint(0, len(l), n)
    return [l[i] for i in indices]

def get_means(d, keys):
    return np.array([np.mean(d[k]) for k in keys], ndim=2)

def get_similarity(arr1, arr2, cov):
    num = np.matmul(arr1.transpose(), np.matmul(cov, arr2))
    den1 = np.matmul(arr1.transpose(), np.matmul(cov, arr1))
    den2 = np.matmul(arr2.transpose(), np.matmul(cov, arr2))
    return num/np.sqrt(np.matmul(den1, den2))

def get_norms(X, cov):
    res = np.diagonal(np.matmul(X, np.matmul(cov, X.transpose())))
    return np.sqrt(res.reshape((len(res),1)))

def get_S(X, Xtest):
    cov = np.inverse(np.cov(X.transpose()))
    xt_c_x = np.matmul(Xtest, np.matmul(cov, X.transpose()))
    Xnorms = get_norms(X, cov)
    Xtnorms = get_norms(Xtest, cov)
    denominator = np.matmul(Xtnorms, Xnorms.transpose())
    return np.divide(xt_c_x, denominator)

def select_games_by_similarity(current_team, X,  S, scale=1, logit_scale=5):
    randomness = np.random.uniform(0,1,size=X.shape[0])
    similarity = S[current_team,:]
    similarity = np.reciprocal(1+np.exp(logit_scale*similarity))
    similarity = similarity * scale
    indices = randomness < similarity
    return (X[indices,:], y[indices], Z[indices,:])



train_year = "2012"

X_team = get_team_features(train_year)
X_defenders = get_cb_features(train_year)
X_receivers = get_wr_features(train_year)

team_similarity_matrix = get_S(X_team, X_team)




