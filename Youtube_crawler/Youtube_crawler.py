from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time

# 크롬 브라우저 조작을 위한 모듈
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# 유튜브 인기 동영상의 댓글 크롤링. 모든 동영상의 모든 댓글 크롤링 가능
if __name__ == "__main__":
    url = 'https://www.youtube.com/feed/trending'

    # 드라이버 불러오기, 페이지 이동
    driver_path = "./chromedriver.exe"
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

    for url in comment_urls:
        # comment_url 로 이동하기
        driver.get(url)
        time.sleep(2)

        # 오류 시 계속 진행하기 위한 try문
        try:
            # 동영상 일시정지 누르기
            driver.find_element(By.XPATH, """//*[@id="movie_player"]/div[1]/video""").click()
            # 페이지 소스 및 제목 가져오기
            comment = BeautifulSoup(driver.page_source, "lxml")
            title = comment.find('yt-formatted-string', 'style-scope ytd-video-primary-info-renderer').get_text()
            
            control = driver.find_element(By.TAG_NAME,"body")
            step = 1

            # 시작 시간 체크
            start = datetime.now()
            # url_num 1증가
            url_num += 1
            # 댓글 시작 알림
            print("=" * 60)
            print("수집을 시작합니다. Title<%d> : %s" % (url_num, title))

            # scroll 끝까지 내리기
            control.send_keys(Keys.PAGE_DOWN)
            control.send_keys(Keys.PAGE_DOWN)
            control.send_keys(Keys.PAGE_DOWN)
            time.sleep(1.5)

            # 댓글 수 세기
            last_comment_count = len(comment.find_all('yt-formatted-string', id='content-text'))

            # while True = 모든 댓글을 끝까지 수집
            while True:
                # 스크롤 끝까지 내리기
                for x in range(4):
                    control.send_keys(Keys.PAGE_DOWN)
                # load 시간 기다리기
                time.sleep(2)

                # new_comment_count를 센 후 저번 last_comment_count와 비교
                comment = BeautifulSoup(driver.page_source, "lxml")
                new_comment_count = len(comment.find_all('yt-formatted-string', id='content-text'))
                # 전부 가져왔을 때 루프 종료
                if new_comment_count == last_comment_count:
                    break

                print("step = %d, last_comment_count = %d, new_comment_count = %d" % (
                step, last_comment_count, new_comment_count))
                step += 1
                last_comment_count = new_comment_count

            # comment 가져오기
            comment = comment.find_all('yt-formatted-string', id='content-text')
            for y in range(new_comment_count):
                comment_sum.append(
                    comment[y].get_text().replace('\ufeff', '').replace('\n', '').replace('\w', '').replace('\r', ''))
                title_sum.append(title)

            # 종료 시간 체크
            end = datetime.now()
            time_taken = end - start
            time_taken_total = end - start_total

            # 수집 종료 알림
            print("=" * 60)
            print("수집이 끝났습니다.")
            print('이번 계산 시간 : ', end='')
            print(time_taken)
            print('이번 수집 개수 : %d' % new_comment_count)
            print('현재까지 총 계산 시간 : ', end='')
            print(time_taken_total)
            print('현재까지 총 수집 개수: %d개' % (len(comment_sum)))

        # except 문(오류시 다음 ulr로 넘어가서 진행)
        except:
            print('Error 발생! 다음 url로 넘어갑니다.')
            continue

    # 모든 수집 완료 알림, csv로 저장
    print("=" * 60)
    print("모든 수집을 완료했습니다.")
    pd.Series(comment_sum).to_frame(name='Youtube_comments').to_csv('Youtube_comments.csv')
