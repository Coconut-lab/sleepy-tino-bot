import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime

def station(num):
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query='
    station = ''
    # #사용자에게 입력받은 값으로 역 설정
    while 1:
        if num == "1" :
            station = "정왕역막차"
            break
        elif num == "2" :
            station = "정왕역수인분당선막차"
            break

    last_canival = []
    url += station
    now = datetime.now()
    dr = webdriver.Chrome()
    dr.get(url)
    time.sleep(3.5)
    source = dr.page_source
    bs = BeautifulSoup(source, 'lxml')
    station_time = bs.find_all('strong',{'class' : 'time'})
    station_lines = bs.find_all('em', {'class':'station'})
    cnt = 0
    cout_cnt = 0
    j = 0
    for tm in range(0,len(station_time)):
        st_tms = station_time[tm].get_text()
        st_tm = [int(st_tms[0:2]), int(st_tms[3:5])]
        if int(st_tms[0:2]) == 0:
            st_tm[0] = 24
        if station_lines[j].get_text() == '당고개' or station_lines[j].get_text() == '왕십리':
            j += 2
            continue
        elif st_tm[0] < now.hour or st_tm[0] == now.hour and st_tm[1] < now.minute:
                j += 2
                continue
        else:
            if cnt == 2:
                break
            else:
                last_canival.append(station_time[tm].get_text() + " " + station_lines[j].get_text() + ' -> ' + station_lines[j+1].get_text())
                j += 2
                cout_cnt += 1
                cnt += 1


    dr.quit()

    return last_canival
