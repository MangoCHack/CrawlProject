# -*- coding: utf-8 -*-
import scrapy
import requests
import os
from urllib.parse import urlparse
from PIL import Image, ImageSequence
from urllib.request import urlopen
from io import BytesIO
from util.utils import get_ip, initialize_database, select_all_fullurls, initialize_database2, select_all_urls, detect_text_uri, connect_database, detect_text

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


keywords = ['코드', '가입', '카지노', '스포츠', '라이브', '전용', '고액', '상한', '호텔', '신규', '국내', '돌발', '놀이터',\
            '해외', '배당', '가입코드', '문의', '안전', '업체', '메이저', '가능', '이벤트', '천만', '게임', '매충', '사이트', '국내배당',\
            '돌발', '다양', '지급', '배팅', '보증', '포커', '경기', '미니', '천만원고액전용', '최고', '노리', '최대', '실시간', '제재',\
            '인플레이', '진행', '환전', '미니게임', '스포츠상한', '매출', '무제', '유럽식', '리얼', '링크', '광고', '검증', '충전',\
            '머니', '유럽식스포츠', '매일', '시간', '쿠폰', '가지', '그램', '보증업체', '무료', '성인', '라이브포커', '호텔카지노',\
            '인증', '총판', '주말', '정식', '먹튀', '모든', '오버', '제한', '토토', '동일', '추천', '핸디캡', '총판문의', '주소',\
            '보기', '정보', '오버가능', '렌트', '보너스', '영상', '제휴', '공식', '무제한', '우리', '해외', '파트너', '베팅',\
            '시리즈', '고객', '상품', '업계',  '루틴', '세계', '단폴', '입금', '모음', '토렌트', '파워볼', '신규가입', '무한', '전무',\
            '라이센스', '커뮤니티',  '상한가', '완료', '시스템', '가입머니', '클릭', '보증금', '전세계', '먹튀검증', '각종', '텔레그램',\
            '예치', '회원', '용품', '증정', '즉시', '시청', '출석', '센터', '당첨', '구매', '고액전용노리터', '발매', '무사고', '비아그라',\
            '전국', '방송', '전화', '중계', '바나나몰', '명기', '일본', '판매', '웹툰', '놀이터코드', '티비', '배팅가능', '당일', '증명',\
            '한국', '리얼돌', '획득', '다운로드', '자동', '연속', '분석', '포인트', '더블', '상담', '승인', '션카지노', '도입', '제외', '제제',\
            '성인용품', '이브', '전신', '전문', '바카라', '각종문의', '이터', '총집합', '크로스', '혜택', '야동', '도박', '수익', '오르가즘', '업소',\
            '배송', '비밀보장', '할인', '애니', '드라마', '마약', '슬롯']

class SitesPySpider(scrapy.Spider): 
    name = 'sites'
    allowed_domains = ['mangacat2.net']
    start_urls = ['https://mangacat2.net/']

    def __init__(self, *args, **kargs):
        dbConnect = connect_database("illegals.db")
        self.startUrls = select_all_urls(dbConnect)
        self.dbConnectStore = initialize_database2('sites_connection_unlimited.db') # 결과물 DB 저장 초기화
        
        self.mainIPs = []
        self.resultUrls = []
        self.repUrls = []
        self.tmpDir = 'tmpimage'
        self.driver='.\\drivers\\chromedriver.exe'
        os.makedirs(self.tmpDir, exist_ok=True)
        
    def start_requests(self):
        for url in self.startUrls:
            yield scrapy.Request(url = url, callback= self.link_parse, method='GET', encoding = 'utf=8')

    def link_parse(self, response):
        baseIP = get_ip(response.url)
        if baseIP in self.mainIPs:
            yield None
        self.mainIPs.append(baseIP)
        print(response.url, baseIP)

        images = response.css('a[href] > img') # a 태그 하이퍼 링크 있는 이미지
        links = []
        for image in images:
            imageSrc = image.css('img::attr(src)').get()
            if imageSrc.startswith('http'):
                imageUrl = imageSrc
            else:
                imageUrl = response.urljoin(imageSrc) #a 태그 하이퍼 링크 -> 이미지 링크
            link = image.xpath('..').css('a::attr(href)').re(r'http.*')[0] # 이지미링크에 연결된 하이퍼링크
            if not link:
                link = image.xpath('..').css('a::attr(href)').re(r'*php*|*javascript*')
                #javascript 등을 통해 연결되는 경우, 주소가 코드에 적혀있지 않을경우 수집 방법 -> selenium 사용하여 클릭 후 주소 획득(속도??)
                #개발자도구 - 네트워크 - xhr 파일을 보면 json형태로 javascript:void(0)로 연결되는 주소가 적혀있는 경우가 있음
                if link:# php나 javascript를 통한 링크추출
                    #동적페이지 호출
                    options = webdriver.ChromeOptions()
                    options.add_argument('headless')
                    options.add_argument('window-size=1920x1080')
                    options.add_argument("disable-gpu")
                    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
                    options.add_argument("lang=ko_KR")
                    driver = webdriver.Chrome(executable_path=self.driver,chrome_options=options)
                    driver.get(url=response.url)
                    #xpath 경로 구해야함.. image.xpath('..')의 xpath 경로
                    driver.find_element_by_xpath().click() # <---- xpath만 구하면 됨
                    driver.switch_to.window(driver.window_handles[-1])
                    link = driver.current_url
                    driver.quit()

            if link:
                text = ''
                if imageUrl.endswith('gif'):
                    index = 1
                    try:
                        imageBytes = requests.get(imageUrl,stream=True)
                        imageBytes.raw.decode_content = True
                        im = Image.open(imageBytes.raw)
                    except Exception as e1:
                        print("[-] image extract fail : " + str(e1))
                        try:
                            im = Image.open(urlopen(imageUrl))
                        except Exception as e2:
                            print("[-] image extract all fail : " + str(e2))
                            print("[-] image url " + imageUrl)
                            continue

                    try:
                        for frame in ImageSequence.Iterator(im):
                            frame.save(f'./{self.tmpDir}/{index}.png')
                            text += detect_text(f'./{self.tmpDir}/{index}.png')
                            os.remove(f'./{self.tmpDir}/{index}.png')
                            index += 1
                            if index > 10:
                                break
                    except Exception as e3:
                        print("[-] image extract fail : " + str(e3))
                        print("[-] extracted text : " + text)
                        continue
                else:
                    text = detect_text_uri(imageUrl)
                if any(word in text for word in keywords): # 추출된 텍스트에 keyword 하나라도 있으면 배너이미지로 인식
                    links.append((imageUrl,link))
            
        imageUrls = []
        for index, link in enumerate(links):
            try:
                ip = get_ip(link[1]) #하이퍼링크
                if ip not in self.mainIPs:
                    if not self.db_check(self.dbConnectStore, baseIP, ip): # DB 확인 후 같은 IP쌍 없으면 추가
                        row = {'main_url':urlparse(response.url).netloc,'main_ip':baseIP,'connect_url':urlparse(link[1]).netloc,'connect_ip':ip}
                        with self.dbConnectStore:
                            cursor = self.dbConnectStore.cursor()
                            sql = f"""
                                INSERT INTO sites_connection VALUES (
                                    \'{row["main_url"]}\',
                                    \'{row["main_ip"]}\',
                                    \'{row["connect_url"]}\',
                                    \'{row["connect_ip"]}\'
                                )
                            """
                            cursor.execute(sql)
                            self.dbConnectStore.commit()
                        imageUrls.append(link[0])
                        print("[+] db store : %s, %s" % (baseIP, ip))
                        print("[+] urls : %s, %s" % (response.url, link[1]))
                        yield scrapy.Request(url = link[1], callback= self.link_parse, method='GET', encoding = 'utf=8')
            except Exception as e:
                print(e)
                continue
        yield {
            'image_urls' : imageUrls
        }

    def db_check(self, dbConnect, mainIP, connectIP):
        try:
            with dbConnect:
                cursor = dbConnect.cursor()

                sql = f"""
                    SELECT 1
                    FROM sites_connection
                    WHERE main_ip = \'{mainIP}\' AND connect_ip = \'{connectIP}\'
                """ # 조건만족시 1 반환

                result = cursor.execute(sql)

                dbConnect.commit()
        except Exception as e:
                print(e)
        return True if len(result.fetchall()) > 0 else False
