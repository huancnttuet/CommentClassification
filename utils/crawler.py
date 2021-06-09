from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import re
from bs4 import BeautifulSoup
import urllib
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import csv


def load_url_selenium_lazada(url):
    # Selenium
    driver = webdriver.Chrome(ChromeDriverManager().install())
    print("Loading url=", url)
    driver.get(url)
    list_review = []
    # just craw 10 page
    x = 0
    while x < 10:
        try:
            # Get the review details here
            WebDriverWait(driver, 5).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.item")))
        except:
            print('No has comment')
            break

        product_reviews = driver.find_elements_by_css_selector(
            "[class='item']")
        # Get product review
        for product in product_reviews:
            review = product.find_element_by_css_selector(
                "[class='content']").text
            if (review != "" or review.strip()):
                print(review, "\n")
                list_review.append(review)
        # Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
        if len(driver.find_elements_by_css_selector("button.next-pagination-item.next[disabled]")) > 0:
            break
        else:
            button_next = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button.next-pagination-item.next")))
            driver.execute_script("arguments[0].click();", button_next)
            print("next page")
            time.sleep(2)
            x += 1
    driver.close()
    return list_review


def load_url_selenium_tiki(argument, start=0, comments_file=""):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1500,944")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options)

    list_reviews = []
    i = 0
    for product in argument:
        i += 1
        if(i < start):
            continue
        product_name = product[0]
        url = product[1]
        print("Loading url=", url)
        driver.get(url)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # just craw max 100 page
        x = 0
        while x < 1000:
            try:
                # Get the review details here
                WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.review-comment")))
            except:
                print('Not has comment!')
                break

            product_reviews = driver.find_elements_by_class_name(
                "review-comment")

            # Get product review
            for product in product_reviews:

                user_name = product.find_element_by_css_selector(
                    "[class='review-comment__user-name']").text
                print(user_name)
                user_date = product.find_element_by_css_selector(
                    "[class='review-comment__user-date']").text

                user_info1 = product.find_elements_by_css_selector(
                    "[class='review-comment__user-info']")[0].find_elements_by_tag_name("span")[0].text
                user_info2 = product.find_elements_by_css_selector(
                    "[class='review-comment__user-info']")[1].find_elements_by_tag_name("span")[0].text

                comment_rating = product.find_elements_by_class_name(
                    "review-comment__rating")
                comment_rating_div = comment_rating[0].find_elements_by_tag_name(
                    "div")
                star_text = comment_rating_div[0].get_attribute('style')
                star_rating = convert_to_star_rating(star_text)

                comment_created_div = product.find_elements_by_class_name(
                    "review-comment__created-date")
                comment_created_span = comment_created_div[0].find_elements_by_css_selector(
                    "*")
                comment_created = comment_created_span[0].text
                # time_used = ""
                # if(len(comment_created_span) == 2):
                #     time_used = comment_created_span[1].text

                comment_thanks_span = product.find_elements_by_class_name(
                    'review-comment__thank')
                comment_thanks = comment_thanks_span[0].find_elements_by_tag_name(
                    "span")
                number_like = "0" if re.findall(
                    '\d+', comment_thanks[0].text) == [] else re.findall('\d+', comment_thanks[0].text)[0]

                review = product.find_element_by_css_selector(
                    "[class='review-comment__content']").text
                if (review != "" or review.strip()):
                    print(review, "\n")
                    list_reviews.append([product_name, user_name, user_date,
                                         user_info1, user_info2,
                                         review,
                                         comment_created,
                                         number_like, star_rating])
            # Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
            try:
                # button_next = driver.find_element_by_xpath(
                #     "//li[@class='btn next']/a").click()
                button_next = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, "//a[@class='btn next']")))
                print(button_next)
                if button_next is None or button_next == []:
                    break
                driver.execute_script("arguments[0].click();", button_next)
                time.sleep(5)
                print("next page")
                print(url)
                x += 1
            except (TimeoutException, WebDriverException) as e:
                print('Load several page!')
                break
        # with open(comments_file + '\comment%d.txt' % start, 'a', encoding="utf-8") as f:
        #     for comment in list_reviews:
        #         f.write(comment[0] + "," + comment[1] + "," + comment[2] + "," +
        #                 comment[3] + "," + comment[4] + "," + comment[5] + "," + comment[6] + "," + comment[7] + "," + comment[8] + "\n")
        #     f.close()
        if len(list_reviews) != 0:
            with open(comments_file + '\comment%d.csv' % start, 'a', newline='', encoding="utf-8") as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                for comment in list_reviews:
                    wr.writerow(comment)
            list_reviews = []

    driver.close()
    print("Total:%d" % len(list_reviews))

    return list_reviews


def convert_to_star_rating(argument):
    switcher = {
        "width: 100%;": "5",
        "width: 80%;": "4",
        "width: 60%;": "3",
        "width: 40%;": "2",
        "width: 20%;": "1",
    }

    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return switcher.get(argument, "0")


def load_url(url):
    print("Loading url=", url)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    script = soup.find_all("script", attrs={"type": "application/ld+json"})[0]
    script = str(script)
    script = script.replace(
        "</script>", "").replace("<script type=\"application/ld+json\">", "")

    csvdata = []

    for element in json.loads(script)["review"]:
        if "reviewBody" in element:
            csvdata.append([element["reviewBody"]])

    return csvdata


def crawl_products(url):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1500,944")

    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options)
    print("Loading url=", url)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    list_product = []
    x = 0
    while x < 1000000:

        products = driver.find_elements_by_class_name(
            "product-item")
        for product in products:
            product_link = product.get_attribute("href")
            product_name = product.find_element_by_css_selector(
                "[class='name']").text
            print(product_name)
            print(product_link)
            list_product.append([product_name, product_link])
        try:
            button_nexts = driver.find_elements_by_xpath(
                "//a[@data-view-id='product_list_pagination_item']")
            if(len(button_nexts) == 4 or len(button_nexts) == 0):
                break
            button_nexts[len(button_nexts) - 1].click()
            time.sleep(2)
            print("next page ")
            print(x)
            x += 1
        except (TimeoutException, WebDriverException) as e:
            print('Load several page!')
            return list_product

    driver.close()
    return list_product


def crawl_products_shopee(url, output_file):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1500,944")

    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options)
    print("Loading url=", url)
    driver.get(url)

    list_product = []
    x = 0
    while x < 100:

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-5000);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-4500);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-4000);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-3500);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-2800);")
        time.sleep(1)
        try:
            # Get the review details here
            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, "div.shopee-search-item-result__item")))
        except:
            print('Not has products!')
            break

        products = driver.find_elements_by_class_name(
            "shopee-search-item-result__item")
        for product in products:
            product_link = product.find_element_by_css_selector(
                "[data-sqe='link']").get_attribute("href")
            product_name = product.find_element_by_css_selector(
                "[data-sqe='name']").text
            # print(product_name.split('\n')[0])
            # print(product_link)
            list_product.append([product_name.split('\n')[0], product_link])
        try:
            # button_next = driver.find_element_by_class_name(
            #     "shopee-icon-button--right")
            # button_next.click()
            button_next = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button.shopee-icon-button--right")))
            driver.execute_script("arguments[0].click();", button_next)
            time.sleep(2)
            print("next page ")
            print(x)
            x += 1
        except (TimeoutException, WebDriverException) as e:
            print('Load several page!')
            with open(output_file, 'a', newline='', encoding="utf-8") as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                for p in list_product:
                    wr.writerow(p)

        with open(output_file, 'a', newline='', encoding="utf-8") as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for p in list_product:
                wr.writerow(p)

    driver.close()
    return list_product


def load_url_selenium_shopee(argument, comments_file=""):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1500,944")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options)

    list_reviews = []
    i = 0
    for product in argument:
        i += 1
        product_name = product[0]
        url = product[1]
        print("Loading url=", url)
        driver.get(url)
        time.sleep(3)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-1800);")
        # just craw max 100 page
        x = 0
        page = 0
        while x < 50:
            try:
                # Get the review details here
                WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.shopee-product-comment-list")))
            except:
                print('Not has comment!')
                break

            product_reviews = driver.find_elements_by_class_name(
                "shopee-product-rating__main")
            print(len(product_reviews))
            # Get product review
            for product in product_reviews:
                user_name = product.find_element_by_css_selector(
                    "[class='shopee-product-rating__author-name']").text
                created_at = product.find_element_by_css_selector(
                    "[class='shopee-product-rating__time']").text
                start_div = product.find_elements_by_class_name(
                    "icon-rating-solid--active")
                rate = len(start_div)

                review = product.find_element_by_css_selector(
                    "[class='shopee-product-rating__content']").text

                if ((review != "" or review.strip()) and review != "****** Đánh giá đã bị ẩn do nội dung không phù hợp. ******"):
                    print(review, "\n")
                    list_reviews.append([product_name, user_name, created_at,
                                         review, rate
                                         ])
            # Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
            try:
                # button_next = driver.find_element_by_xpath(
                #     "//li[@class='btn next']/a").click()
                button_next = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button.shopee-icon-button--right")))
                button_current = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button.shopee-button-solid--primary")))

                print(page)
                if(page == int(button_current.text)):
                    break
                else:
                    page = int(button_current.text)
                driver.execute_script("arguments[0].click();", button_next)
                time.sleep(2)
                print("next page")
                print(url)
                x += 1
            except (TimeoutException, WebDriverException) as e:
                print('Load several page!')
                break

        if len(list_reviews) != 0:
            with open(comments_file, 'a', newline='', encoding="utf-8") as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                for comment in list_reviews:
                    wr.writerow(comment)
            list_reviews = []

    driver.close()
    print("Total:%d" % len(list_reviews))

    return list_reviews


def load_url_selenium_shopee_by_rating(links=[], comments_file="", rate=2):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1500,944")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options)

    list_reviews = []
    i = 0
    for product in links:
        i += 1
        product_name = product[0]
        url = product[1]
        print("Loading url=", url)
        driver.get(url)
        time.sleep(3)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-1000);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-2000);")
        time.sleep(1)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight-3000);")
        # just craw max 100 page
        x = 0
        page = 0
        while x < 50:
            try:
                # Get the review details here
                WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.shopee-product-comment-list")))
            except:
                print('Not has comment!')
                break

            try:
                rating_div = driver.find_elements_by_class_name(
                    "product-rating-overview__filter")

                if rate == 5:
                    rating_div[1].click()
                elif rate == 4:
                    rating_div[2].click()
                elif rate == 3:
                    rating_div[3].click()
                elif rate == 2:
                    rating_div[4].click()
                elif rate == 1:
                    rating_div[5].click()
                time.sleep(2)
                print("rate page : %d " % rate)
            except (TimeoutException, WebDriverException) as e:
                print('Load several page!')

            try:
                # Get the review details here
                WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.shopee-product-comment-list")))
            except:
                print('Not has comment!')
                break

            product_reviews = driver.find_elements_by_class_name(
                "shopee-product-rating__main")

            # Get product review
            for product in product_reviews:
                user_name = product.find_element_by_css_selector(
                    "[class='shopee-product-rating__author-name']").text
                created_at = product.find_element_by_css_selector(
                    "[class='shopee-product-rating__time']").text
                start_div = product.find_elements_by_class_name(
                    "icon-rating-solid--active")
                rate = len(start_div)

                review = product.find_element_by_css_selector(
                    "[class='shopee-product-rating__content']").text

                if ((review != "" or review.strip()) and review != "****** Đánh giá đã bị ẩn do nội dung không phù hợp. ******"):
                    print(review, "\n")
                    list_reviews.append([product_name, user_name, created_at,
                                         review, rate
                                         ])
            try:

                button_next = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button.shopee-icon-button--right")))
                button_current = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button.shopee-button-solid--primary")))

                print(page)
                if(page == int(button_current.text)):
                    break
                else:
                    page = int(button_current.text)
                driver.execute_script("arguments[0].click();", button_next)
                time.sleep(2)
                button_current = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "button.shopee-button-solid--primary")))

                if(int(button_current.text) == 1):
                    break
                print("next page")
                print(url)
                x += 1
            except (TimeoutException, WebDriverException) as e:
                print('Load several page!')
                break

        if len(list_reviews) != 0:
            with open(comments_file, 'a', newline='', encoding="utf-8") as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                for comment in list_reviews:
                    wr.writerow(comment)
            list_reviews = []

    driver.close()
    print("Total:%d" % len(list_reviews))

    return list_reviews
