from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By

comments = []
url_list = pd.read_csv('ilbe_url_list.csv')['url'].tolist()

i = 1185
driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
for url_num in range(i, len(url_list)):
    driver.get(url_list[url_num])
    comment_list = driver.find_elements(By.XPATH, '//span[contains(@class, \'comment-box\')]')
    for comment in comment_list:
        comments.append(comment.text)
        print(url_num, comment.text) 
    pd.Series(comments).to_frame(name='ilbe_comment').drop_duplicates().reset_index(drop=True).to_csv('ilbe_comments.csv', index=False)           
    time.sleep(2)
