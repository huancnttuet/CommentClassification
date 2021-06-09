import pickle
from sklearn.feature_selection import SelectKBest, f_regression, chi2
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer

X_data = pickle.load(open('datamining\data\shopee\X_data.pkl', 'rb'))
y_data = pickle.load(open('datamining\data\shopee\y_data.pkl', 'rb'))

emb = TfidfVectorizer(min_df=5, max_df=1.0,
                      max_features=3000, sublinear_tf=True)
X = emb.fit_transform(X_data)

print(emb.get_feature_names())
print(X.shape)
y = y_data
X_new = SelectKBest(chi2, k=20).fit_transform(X, y)

print(X_new.shape)





# from sklearn.datasets import load_iris
# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import chi2
# X, y = load_iris(return_X_y=True)
# print(X[0])
# X_new = SelectKBest(chi2, k=2).fit_transform(X, y)
# print(X_new.shape)
