import csv

from utils.crawler import load_url_selenium_shopee_by_rating

from configs import ROOT_DIR

products_file = ROOT_DIR + '\outputs\category\shopee\\may-tinh-laptop.csv'
comments_file = ROOT_DIR + '\outputs\comments\shopee\\1\\may-tinh-laptop-comments.csv'

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

comments = load_url_selenium_shopee_by_rating(
    links=uniqueData, comments_file=comments_file, rate=1)

# print(len(comments))
# create_comment_file(comments_file + '\comment%d.xlsx' % start, comments)
