
import csv
from configs import ROOT_DIR
from utils.crawler import crawl_products, crawl_products_shopee
from utils.excel import create_product_file

# url = "https://tiki.vn/may-giat/c3862"
# url = "https://tiki.vn/dien-tu-dien-lanh/c4221"
# url = "https://shopee.vn/%C4%90i%E1%BB%87n-tho%E1%BA%A1i-cat.84.1979"
# url = "https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.78"
# url = "https://shopee.vn/Th%E1%BB%9Di-Trang-N%E1%BB%AF-cat.77"
# url = "https://shopee.vn/B%C3%A1ch-Ho%C3%A1-Online-cat.9824"
# url = "https://shopee.vn/S%E1%BA%A3n-Ph%E1%BA%A9m-Kh%C3%A1c-cat.91"
url = "https://shopee.vn/M%C3%A1y-t%C3%ADnh-Laptop-cat.13030"
output_file = ROOT_DIR + '\outputs\category\shopee\\may-tinh-laptop.csv'

products = crawl_products_shopee(url=url, output_file=output_file)


# create_product_file(output_file, products)
