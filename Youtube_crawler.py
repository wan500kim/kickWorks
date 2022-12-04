from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time

# 유튜브 인기 동영상의 댓글 크롤링. 모든 동영상의 모든 댓글 크롤링 가능
if __name__ == "__main__":
    url = 'https://www.youtube.com/feed/trending'

    # 드라이버 불러오기, 페이지 이동
    driver_path = "C:/Users/pych/Desktop/VSC_python/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    time.sleep(2)
    driver.get(url)
    time.sleep(4)

    # 페이지 소스 가져오기
    data = BeautifulSoup(driver.page_source, "lxml")
    # comment_urls 리스트 만들기
    comment_urls = []
    # 영상 타이틀을 눌렀을 때 다이렉트 되는 주소를 수집
    for x in range(len(data.find_all('a', 'yt-simple-endpoint style-scope ytd-video-renderer'))):
        comment_urls.append('https://www.youtube.com/'+ data.find_all('a', 'yt-simple-endpoint style-scope ytd-video-renderer')[x]['href'])

    # 댓글들을 담을 리스트
    title_sum = []
    comment_sum = []
    url_num = 0
    # 총 시작시간 체크
    start_total = datetime.now()

    # 전체 동영상 개수 세기
    a = 0
    for url in comment_urls:
        a = a + 1
    print("전체 동영상 개수: [%d]개" % a)
