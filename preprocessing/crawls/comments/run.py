import pandas as pd
from utils.crawler import load_url_selenium_tiki
from utils.excel import create_comment_file
from configs import ROOT_DIR

products_file = ROOT_DIR + '\outputs\category\dien-tu-dien-lanh\dien-tu-dien-lanh2.xlsx'
comments_file = ROOT_DIR + '\outputs\comments\dien-tu-dien-lanh'
dfs = pd.read_excel(products_file)

products = dfs.to_numpy()


comments = []
start = 3775

comments = load_url_selenium_tiki(products, start, comments_file)

print(len(comments))
# create_comment_file(comments_file + '\comment%d.xlsx' % start, comments)
