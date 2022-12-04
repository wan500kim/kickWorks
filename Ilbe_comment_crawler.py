from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By

#hate_speech_list = pd.read_csv('hate_speech_raw_data.csv')['hate_speech'].tolist()
hate_speech_list = []
url_list = pd.read_csv('url_list_v2.csv')['url'].tolist()

i = 1185
driver = webdriver.Chrome(executable_path = 'C:/Users/pych/Desktop/VSC_python/chromedriver.exe')
for url_num in range(i, len(url_list)):
    driver.get(url_list[url_num])
    comment_list = driver.find_elements(By.XPATH, '//span[contains(@class, \'comment-box\')]')
    for comment in comment_list:
        hate_speech_list.append(comment.text)
        print(url_num, comment.text) 
    pd.Series(hate_speech_list).to_frame(name='hate_speech').drop_duplicates().reset_index(drop=True).to_csv('hate_speech_raw_data.csv', index=False)           
    time.sleep(2)