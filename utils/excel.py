import xlsxwriter
import csv


def create_comment_file(filename, comments):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    for product_name, user_name, user_date, user_info1, user_info2, review, comment_created, number_like, star_rating in comments:

        worksheet.write(row, col, product_name)
        worksheet.write(row, col+1, user_name)
        # check isNaN
        worksheet.write(
            row, col+2, '' if isinstance(user_date, float) else user_date)
        worksheet.write(row, col+3, user_info1)
        worksheet.write(row, col+4, user_info2)
        worksheet.write(row, col+5, review)
        worksheet.write(row, col+6, comment_created)
        # worksheet.write(row, col+7, '' if math.isnan(time_used) else time_used)
        worksheet.write(row, col+7, number_like)
        worksheet.write(row, col+8, star_rating)
        row += 1
    workbook.close()


def create_product_file(filename, products):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    for product_name, link in products:
        worksheet.write(row, col, product_name)
        worksheet.write(row, col+1, link)

        row += 1
    workbook.close()


def read_file_csv(dataset_file_path):

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
    return [data_1, data_2, data_3, data_4, data_5]