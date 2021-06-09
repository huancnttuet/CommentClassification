import pandas as pd
from configs import ROOT_DIR
from utils.transformer import standardize_data, tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
import numpy as np
import csv
import pickle


dataset_file_path = ROOT_DIR + '\outputs\comments\dienthoai\\all.xlsx'
df = pd.read_excel(dataset_file_path)
# comments = df.iloc[:, 5]
# rates = df.iloc[:, 8]

comments = np.array(df)
comments = comments.tolist()
# comments = comments.apply(standardize_data)
# comments = comments.apply(tokenizer)


print(comments[0])
comments = [[r[0], r[1], r[2], r[3], r[4],
             r[5], r[6], str(r[7]), str([8])]for r in comments]
dataset_file_path = ROOT_DIR + '\outputs\comments\dien-tu-dien-lanh-all\\all.csv'
with open(dataset_file_path, encoding="utf-8") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    # next(reader, None)  # skip the headers
    data_read = [row for row in reader]

comments.extend(data_read)
print(data_read[0])

print(len(comments))
X = [[r[0], r[1], r[2], r[3], r[4],
      tokenizer(standardize_data(r[5])), r[6], r[7]]for r in comments]
y = [r[8] for r in comments]

save_file_path = ROOT_DIR + '\datamining\datazip'


pickle.dump(X, open(save_file_path + '\X_data.pkl', 'wb'))
pickle.dump(y, open(save_file_path + '\y_data.pkl', 'wb'))

print(len(comments))
print(comments[1])
