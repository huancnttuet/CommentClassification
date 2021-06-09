import csv
from utils.transformer import standardize_data
from utils.excel import create_comment_file
import pandas as pd
from configs import ROOT_DIR
from os import walk

files = []
files2 = []
folder_path = ROOT_DIR + '\outputs\comments\dien-tu-dien-lanh'
folder_path2 = ROOT_DIR + '\outputs\dienthoai3'
for (dirpath, dirnames, filenames) in walk(folder_path):
    files.extend(filenames)
    break

# for (dirpath, dirnames, filenames) in walk(folder_path2):
#     files2.extend(filenames)
#     break

comments = []
for f in files:
    with open(folder_path + "\\" + f, encoding="utf-8") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        # next(reader, None)  # skip the headers
        data_read = [row for row in reader]

    comments.extend(data_read)

# Read CSV file


# comments2 = []
# for f in files2:
#     df = pd.read_excel(folder_path2 + "\\" + f)
#     if len(df) == 0:
#         continue
#     comments2.extend(df.to_numpy())


# comments.extend(comments2)

save_file = ROOT_DIR + '\outputs\comments\dien-tu-dien-lanh-all\\all.csv'


# create_comment_file(save_file, comments)

with open(save_file, 'a', newline='', encoding="utf-8") as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for comment in comments:
        wr.writerow(comment)

# standardize_comments = []
# for comment in comments:
#     standardize_comments.extend([standardize_data(comment)])
