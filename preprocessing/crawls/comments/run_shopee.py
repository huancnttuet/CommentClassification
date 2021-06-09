import csv
from enum import unique

from utils.crawler import load_url_selenium_shopee
import numpy as np
from configs import ROOT_DIR

products_file = ROOT_DIR + '\outputs\category\shopee\\thoi-trang-nu.csv'
comments_file = ROOT_DIR + '\outputs\comments\shopee\\thoi-trang-nu-comments.csv'

with open(products_file, encoding="utf-8") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    # next(reader, None)  # skip the headers
    data_read = [row for row in reader]

print(len(data_read))
uniqueData = []
for r in data_read:
    if r not in uniqueData:
        uniqueData.append(r)

print(len(uniqueData))

comments = []
print(data_read[0])
comments = load_url_selenium_shopee(uniqueData, comments_file)

# print(len(comments))
# create_comment_file(comments_file + '\comment%d.xlsx' % start, comments)
