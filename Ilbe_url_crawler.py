from selenium import webdriver
import time
import pandas as pd

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

list_size = 10000
url = 'https://www.ilbe.com/list/ilbe?listSize={}&sub=best&listStyle=list'.format(list_size)
driver = webdriver.Chrome(executable_path = 'C:/Users/pych/Desktop/VSC_python/chromedriver.exe')
driver.get(url)
time.sleep(5)

url_list = []
post_list = driver.find_elements(By.XPATH,'//ul[contains(@class, \'board-body\')]//li[not(@id) and not(@class)]//span[contains(@class, \'title\')]//a[contains(@class, \'subject\')]')
for post_num in range(len(post_list)):
    print(post_num, post_list[post_num].get_attribute('href'))
    url_list.append(post_list[post_num].get_attribute('href'))
    pd.Series(url_list).to_frame(name='url').to_csv('C:/Users/pych/Desktop/VSC_python/url_list_v2.csv')