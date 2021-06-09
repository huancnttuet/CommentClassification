import pandas as pd
from configs import ROOT_DIR
from utils.transformer import standardize_data, tokenizer

from sklearn.model_selection import train_test_split
import numpy as np
import csv
import pickle

dataset_file_path = ROOT_DIR + '\outputs\comments\shopee\\thoi-trang-nam-comments.csv'

with open(dataset_file_path, encoding="utf-8") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    # next(reader, None)  # skip the headers
    data_read = [row for row in reader]

data = [[r[3], r[4]] for r in data_read]
data_5 = [r for r in data if r[1] == '5']
data_4 = [r for r in data if r[1] == '4']
data_3 = [r for r in data if r[1] == '3']
data_2 = [r for r in data if r[1] == '2']
data_1 = [r for r in data if r[1] == '1']

print(data_5[0])
print(len(data_5))
print(data_4[0])
print(len(data_4))
print(data_3[0])
print(len(data_3))
print(data_2[0])
print(len(data_2))
print(data_1[0])
print(len(data_1))

results = []

results.extend(data_5)
results.extend(data_4)
results.extend(data_3)
results.extend(data_2)
results.extend(data_1)
print(results[0])
print(len(results))


X = [r[0] for r in results]
y = [r[1] for r in results]

X = [tokenizer(standardize_data(x)) for x in X]
print(X[0])

save_file_path = ROOT_DIR + '\datamining\data\shopee'


pickle.dump(X, open(save_file_path + '\X_data2.pkl', 'wb'))
pickle.dump(y, open(save_file_path + '\y_data2.pkl', 'wb'))
