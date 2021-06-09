import xlsxwriter
import pandas as pd
from configs import ROOT_DIR
from utils.transformer import standardize_data, tokenizer

from sklearn.model_selection import train_test_split
import numpy as np
import csv
import pickle
from utils.excel import read_file_csv
from utils.transformer import unique_data
from utils.pre_train import pre_train
results = []


def pineline(dataset_file_path):
    data = read_file_csv(dataset_file_path)
    results.extend(data[4][:1000])
    results.extend(data[3])
    results.extend(data[2])
    results.extend(data[1])
    results.extend(data[0])
    print(results[0])
    print(len(results))


dataset_file_path = ROOT_DIR + '\outputs\comments\shopee\\dienthoai-comments1.csv'
pineline(dataset_file_path)
dataset_file_path = ROOT_DIR + '\outputs\comments\shopee\\dienthoai-comments.csv'
pineline(dataset_file_path)

pineline(ROOT_DIR + '\outputs\comments\shopee\\1\\bach-hoa-comments.csv')
pineline(ROOT_DIR + '\outputs\comments\shopee\\1\\dien-gia-dung-comments.csv')
pineline(ROOT_DIR + '\outputs\comments\shopee\\1\\thoi-trang-nam-comments.csv')
pineline(ROOT_DIR + '\outputs\comments\shopee\\1\\thoi-trang-nu-comments.csv')

pineline(ROOT_DIR + '\outputs\comments\shopee\\2\\bach-hoa-comments.csv')
pineline(ROOT_DIR + '\outputs\comments\shopee\\2\\dien-gia-dung-comments.csv')
pineline(ROOT_DIR + '\outputs\comments\shopee\\2\\thoi-trang-nam-comments.csv')
pineline(ROOT_DIR + '\outputs\comments\shopee\\2\\thoi-trang-nu-comments.csv')

pineline(ROOT_DIR + '\outputs\comments\shopee\\3\\bach-hoa-comments.csv')
pineline(ROOT_DIR + '\outputs\comments\shopee\\3\\thoi-trang-nam-comments.csv')

pineline(ROOT_DIR + '\outputs\comments\shopee\\4\\thoi-trang-nu-comments.csv')


pineline(ROOT_DIR + '\outputs\comments\shopee\\5\\thoi-trang-nu-comments.csv')


data_5 = [r[0] for r in results if r[1] == '5']
data_4 = [r[0] for r in results if r[1] == '4']
data_3 = [r[0] for r in results if r[1] == '3']
data_2 = [r[0] for r in results if r[1] == '2']
data_1 = [r[0] for r in results if r[1] == '1']

print("5 rate : {}".format(len(data_5)))
print("4 rate : {}".format(len(data_4)))
print("3 rate : {}".format(len(data_3)))
print("2 rate : {}".format(len(data_2)))
print("1 rate : {}".format(len(data_1)))


data_5 = unique_data(data_5)
data_4 = unique_data(data_4)
data_3 = unique_data(data_3)
data_2 = unique_data(data_2)
data_1 = unique_data(data_1)

print("5 rate : {}".format(len(data_5)))
print("4 rate : {}".format(len(data_4)))
print("3 rate : {}".format(len(data_3)))
print("2 rate : {}".format(len(data_2)))
print("1 rate : {}".format(len(data_1)))

data_5 = [[r, "5"] for r in data_5]
data_4 = [[r, "4"] for r in data_4]
data_3 = [[r, "3"] for r in data_3]
data_2 = [[r, "2"] for r in data_2]
data_1 = [[r, "1"] for r in data_1]


data = []
data.extend(data_1)
data.extend(data_2)
data.extend(data_3)
data.extend(data_4)
data.extend(data_5[:2000])

print(len(data))
X = [r[0] for r in data]
y = [r[1] for r in data]

X = [standardize_data(x) for x in X]
print(X[0])

i = 0
comments = []
for x in X:
    if x == "" or len(x) == 0:
        i += 1
        continue
    comments.append([x, y[i]])
    i += 1



# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook(
    ROOT_DIR + '\datamining\data\shopee' + '\data1.xlsx')
worksheet = workbook.add_worksheet()

# Start from the first cell. Rows and columns are zero indexed.
row = 1
col = 0

worksheet.write(0, col,     "comment")
worksheet.write(0, col + 1, "label")

# Iterate over the data and write it out row by row.
for r in comments:
    worksheet.write(row, col,     r[0])
    worksheet.write(row, col + 1, r[1])
    row += 1


workbook.close()

# save_file_path = ROOT_DIR + '\datamining\data\shopee' + '\data.csv'

# with open(save_file_path , 'w', newline='', encoding="utf-8") as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     for comment in comments:
#         wr.writerow(comment)

# X = []
# y = []
# for comment in comments:
#     X.append(tokenizer(comment[0]))
#     y.append(comment[1])

# pickle.dump(X, open(save_file_path + '\X_data2.pkl', 'wb'))
# pickle.dump(y, open(save_file_path + '\y_data2.pkl', 'wb'))
