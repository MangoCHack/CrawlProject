# -*- coding: utf-8 -*-
import scrapy
from ..items import CrawlerItem
import requests
import os
from urllib.parse import urlparse
from PIL import Image, ImageSequence
from urllib.request import urlopen
from io import BytesIO
from util.utils import get_ip, initialize_database, select_all_fullurls, initialize_database2, select_all_urls, detect_text_uri, connect_database, detect_text

import time
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
            '보기', '정보', '오버가능', '렌트', '보너스', '영상', '영화', '제휴', '공식', '무제한', '우리', '해외', '파트너', '베팅',\
            '시리즈', '고객', '상품', '업계',  '루틴', '세계', '단폴', '입금', '모음', '토렌트', '파워볼', '신규가입', '무한', '전무',\
            '라이센스', '커뮤니티',  '상한가', '완료', '시스템', '가입머니', '클릭', '보증금', '전세계', '먹튀검증', '각종', '텔레그램',\
            '예치', '회원', '용품', '증정', '즉시', '시청', '출석', '센터', '당첨', '구매', '고액전용노리터', '발매', '무사고', '비아그라',\
            '방송', '전화', '중계', '바나나몰', '명기', '일본', '판매', '웹툰', '놀이터코드', '티비', '배팅가능', '당일', '증명',\
            '리얼돌', '획득', '다운로드', '자동', '연속', '분석', '포인트', '더블', '상담', '승인', '션카지노', '도입', '제외', '제제',\
            '성인용품', '이브', '전신', '전문', '바카라', '각종문의', '이터', '총집합', '크로스', '혜택', '야동', '도박', '수익', '오르가즘', '업소', '오피',\
            '배송', '비밀보장', '할인', '애니', '드라마', '마약', '슬롯', 'TORRENT', 'CASINO', 'GASINO', 'SPIN', 'DRUG', 'BET', 'SPORT']
            # Todo : keyword 카테고리 구분해서 사이트 특징 구분할 수 있도록 작업
'''
[, , '전용', , '호텔', '신규', '국내', '돌발', ,\
            , , '가능', , '매충', '사이트', ,\
            '돌발', '다양', , '최고', , '최대', '실시간', '제재',\
            , '진행', , '무제', '유럽식', , '링크', '광고', '검증', '충전',\
            , '매일', , '가지', '그램', '보증업체', '무료', , ,\
            '인증', '총판', '주말', '정식', '먹튀', '모든', '오버', , '동일', '추천', '핸디캡', '총판문의', '주소',\
            '보기', '정보', '오버가능', '렌트', , '영상', , '공식', '무제한', '우리', '해외', ,\
            , '고객', , '업계',  '루틴', '세계', '단폴', '입금', '모음', ,, '신규가입', '무한', '전무',\
            '라이센스', '커뮤니티',  '상한가', '완료', '시스템', , '클릭', '보증금', '전세계', '먹튀검증', '각종', '텔레그램',\
            '예치', '회원', , '증정', '즉시', '시청', '출석', '센터', '당첨', '구매', , '발매', '무사고', ,\
            '방송', '전화', '중계', , , '일본', , , '놀이터코드', , , ,\
            , '획득',, '자동', '연속', '분석', , '더블', '상담', '승인', , '도입', '제외', '제제',\
             '전신', '전문', '바카라', '각종문의', , '총집합', '크로스', '혜택', ,, , ,\
            , '비밀보장', '할인', '애니', '드라마', , , , , , 'BET', ]
site_type = {
    '도박' : ['코드', '가입', '카지노', '스포츠', '고액', '상한', '놀이터', '해외', '배당', '가입코드', '문의', '안전', '업체', '지급', '배팅', '보증',\
            '포커', '경기', '미니', '천만원고액전용', '환전', '미니게임', '스포츠상한', '매출', '인플레이', '이벤트', '천만', '게임', '라이브포커', '호텔카지노',\
            '파트너', '베팅', '머니', '유럽식스포츠', '보너스', '시간', '쿠폰', '제한', '토토', '파워볼', 'CASINO', 'GASINO', 'SPIN', '도박', '수익', '당일',\
            '가입머니', '슬롯', 'SPORT', '이터', '노리', '메이저', '국내배당' '배팅가능'   ]
    '성인용품' : ['성인', '상품', '용품', '판매', '배송', '리얼', '오르가즘', '포인트', '리얼돌', '바나나몰']
    '약물' : ['상품', '비아그라', '판매', '배송', 'DRUG', '마약']
    '저작물' : ['영화', '드라마', '제휴', '웹툰', '토렌트', '시리즈', 'TORRENT']
    '성인물' : ['라이브', '명기', '토렌트', '야동', '시리즈', '리얼', '오르가즘', '다운로드', '티비']
    '업소' : ['업소']
    '불법기타' : ['증명', '광고']
}
'''


class SitesPySpider(scrapy.Spider): 
    name = 'sites'
    
    allowed_domains = ['mangacat2.net']
    dbConnect = connect_database("illegals.db")
    start_urls = select_all_urls(dbConnect)
    custom_settings = {
        'CONCURRENT_REQUESTS': 100,
        'ROBOTSTXT_OBEY': False,
        'REACTOR_THREADPOOL_MAXSIZE' : 20,
        #image download folder
        #'IMAGES_STORE' : 'test2'
        'ITEM_PIPELINES' : {
        #'scrapy.pipelines.images.ImagesPipeline' : 1, 
        'crawler.pipelines.CrawlerPipeline': 300
        },
        
        'DEPTH_PRIORITY' : 1,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue'
        
    }

    def __init__(self, *args, **kargs):

        self.startUrls = ['http://01.newsdaum.com','http://fr-71.com','http://hoxyna5.com','http://11toon2.com','http://bamsarang1.me','http://1004x.1004tsts.com','http://69bam2.me','http://gmtv3.com','http://1004cube.com','http://bame.co.kr','http://bbga1.com','http://goltv.co.kr','http://avkim1.com','http://69bam3.me','http://1004ses.com','http://11.xn--he5b93brek8q.com','http://cvmp01.site','http://69bam1.me','http://dojun1.com','http://goodlivetv.com','http://itoons01.com','http://goza1.com','http://aone18.com','http://frz11.com','http://ww1.19bam09.com','https://yadongschool.com','https://www.youtube.com','http://ming-ky.net','https://www.google.co.kr','http://3322bmw.com','http://nb-rd.com','http://ssongssong22.net','http://nb-we.com','http://metoon.co.kr','http://onair.kbs.co.kr','http://safe.ggongt.com','http://partner.rosetv.co.kr','http://nb-fo.com','http://kus78.xyz','http://moatv01.com','http://refice.kr','http://soul-88.com','http://sexbam11.me','http://onair.imbc.com','http://play.sbs.co.kr','http://sns-a7.com','http://sns-x5.com','http://namedtoon58.com','http://sns-x3.com','https://www.dating-enjoy.com','http://tsgirl.net','http://tv.hobbang.net','http://www.bo-zi21.net','http://viptv365.com','http://moneytv24.com','http://www.cast-aa.com','http://www.1004mam.com','https://toonbook.net','http://www.gaogaoxing.com','http://www.x-stream.co.kr','http://sm-mp.com','https://t.me','https://www.linkmoon6.me','http://www.dojun1.com','http://www.ktv-kk4.net','http://www.ktv-tv9.org','http://www.ktv-tv10.org','http://www.torrentreel90.com','http://www.wuritv3.com','http://www.goratv.com','http://www.ktv-tv8.org','http://www.nettv.live','http://www.xn--pq1bj6fu7a45dt3r.com','http://www.ktv-tv11.org','http://www.ioctv24.com','http://www.ktv-tv12.org','http://www.ktv-tv13.org','http://www.kongdda1.net','http://www.todayfreeserver.com','http://yiyagi.cn','http://jane2021.com','http://xn--qh3bx4o.net','http://www.xn--2n1bj7gorrf2j.kr','http://yaserati1.live','http://hostinfo.cafe24.com','https://userserver1.blogspot.com','http://rps718.com','http://yug-no.com','http://mvp3001.com','http://zess1.com','http://www.freecafe02.com','http://tww95.com','http://t-0007.com','http://reb-114.com','https://laundry29.wixsite.com','http://g-old11.com','https://15.torrentube.net','http://vacs49.com','http://akarps.xyz','https://www.pok-ddal5.live','https://www.torrent8.icu','https://99zzz.net','https://anibug.com','https://aqstream.com','https://avkim1.com','https://adulti148.com','https://a58.linktv.biz','https://avshow05.me','https://avgle.com','https://avnori1.com','https://avnori6.com','http://to761.com','http://dn-ao.com','https://b36.koreanz.fun','http://an-29.com','http://hol-03.com','https://www.curekr.com','https://cafe.naver.com','http://bbet2020.com','http://sb1-5.com','https://pandora-club.com','http://mex-av4.com','http://po-kk.com','http://www.vap-we.com','http://mex-vvip1.com','https://www.lover-date.com','https://www.playbetmove.com','https://uuzoa16.com','http://011-011.com','http://hol-555.com','http://joun05.com','https://www.afm88.com','https://bbalissa.com','https://beetorrent7.space','https://beetorrent6.space','http://nb-rv.com','http://red-8585.com','https://blacktoon.net','http://ygd45.com','https://blacktoon106.com','http://ww6.black158.com','https://dhlok.com','https://channel.beetip.com','http://bo-zi19.net','https://bora01.net','https://chunzagirl.net','https://bubbletorrent7.space','https://bubbletorrent6.space','https://linkk.club','https://dongyoungsang.club','https://ddaltong01.com','http://ww38.ddalpark8.com','https://enaver.net','https://e-hentai.org','https://ddmapc.com','https://fjav.net','https://freetoon02.com','https://premium-simba.com','https://oncapan.com','https://fxfx35.com','https://fungky1.com','https://fxfx36.com','https://fxfx37.com','https://fxfx38.com','https://fxfx39.com','https://fxfx41.com','https://fxfx40.com','https://fxfx43.com','http://ww38.funitoon05.com','https://fxfx42.com','https://fxfx46.com','https://fxfx47.com','https://fxfx45.com','https://fxfx44.com','https://fxfx49.com','https://fxfx50.com','https://fxfx48.com','https://fxfx51.com','https://fxfx52.com','https://fxfx53.com','https://fxfx54.com','https://fxfx55.com','https://fxfx56.com','https://girltv6.com','http://ww16.hbtoon.com','https://hitomi.la','https://hiyobi.me','https://gogumaplayer.com','https://gochu01.club','http://gcaa21.com','http://ss-109.com','https://aden.hellfors.kr','https://imax05.com','https://joybam.club','https://jav.guru','https://joge08.com','https://hqporner.com','https://joymaxim.com','https://hotscope.tv','https://kimchi.tv','http://bingre-i.com','https://kktoon35.com','http://ss-448.com','http://www.dwt38.com','https://kpopdeepfakes.net','http://sure398.com','http://xn--tl3br2i87r.com','https://kr18.sogirl.co','https://ktoon53.com','https://magumagu.net','https://m01.kormovie.com','https://major-toon.com','https://ktoon61.com','https://ktoon58.com','https://ktoon59.com','https://ktoon55.com','https://ktoon57.com','https://ktoon56.com','https://manhwa0.com','https://mingkyaa25.com','https://miritoon17.com','https://marumaru.pw','https://mobozi01.me','https://mingkyaa22.com','http://tlo-777.com','https://pigav.com','https://nurito.xyz','https://no1.nobra.xyz','https://www.yg02.net','https://onion03.com','https://popjav.tv','https://pumjaral06.com','https://pumjaral04.com','https://pornxs.com','https://realttv.com','https://q90.iqooqootv.org','https://q90.imybinoo.org','https://rktoon6.com','https://rr-2222.com','http://nfx-001.com','https://sexbam11.me','https://seda8.bet','https://uni88-po.com','https://sexbam10.me','http://coba123.com','https://ghf1zwl.nlvkj03asnfq89i46t786g7atyt0gyw1ui.xyz','https://t42.etvlink.com','https://tazotv15.com','https://tkr01.com','https://tktk34.com','https://tocafe.name','https://torrent-who6.me','https://toptoon.com','https://spin559.com','https://twitter.com','https://torrentlady17.com','https://torrentgaza.com','https://torrentissue25.com','https://torrentlin.net','https://torrenthaja13.com','https://torrenthaja.com','https://torrenthaja6.com','https://torrenthaja26.com','https://torrenthaja4.com','https://torrentpan7.net','https://torrentsee51.com','https://www.fosshub.com','https://torrentsoda6.space','https://torrentsoda7.space','https://torrenttt.net','https://torrenttip19.com','https://torrentube.net','https://tumblso2.com','https://tv10.gongzza.net','https://torrentyoung1.com','https://tv7.barobogo.live','https://torrentyoung.org','https://tv11.gongzza.net','https://tvgori02.com','https://www.instagram.com','https://weeya33.net','https://wfwf134.com','https://wtwt65.com','https://wfwf123.com','https://wfwf128.com','https://wfwf137.com','https://wfwf130.com','https://wfwf126.com','https://wtwt62.com','https://wtwt58.com','https://wtwt66.com','https://wtwt61.com','https://videokim.co','https://wtwt54.com','https://wfwf129.com','https://wtwt57.com','https://wfwf136.com','https://wtwt64.com','https://wfwf141.com','https://wfwf125.com','https://wtwt51.com','https://wfwf135.com','https://wtwt67.com','https://wfwf132.com','https://wtwt49.com','https://wtwt53.com','https://wtwt59.com','https://wfwf133.com','https://wtwt47.com','https://wtwt60.com','https://wfwf127.com','https://wfwf138.com','https://wfwf131.com','https://wtwt55.com','https://wfwf124.com','https://wtwt52.com','https://wfwf142.com','https://wtwt50.com','https://wfwf140.com','https://wfwf122.com','https://wtwt63.com','https://wfwf139.com','https://wtwt56.com','https://v58.baydrama.live','https://wtwt48.com','https://wfwf121.com','https://wantjav.com','https://vjav.com','https://watchjavonline.com','https://wtwt46.com','https://w64.showtv.club','https://www.bananatv15.com','https://www.allall45.net','https://www.4tube.com','https://www.bo-zi21.net','https://www.bbongtv.com','https://www.free-tv4.xyz','https://www.manduya10.com','https://www.lasbet1004.com','https://www.mulsn2020.com','https://www.jogemain.com','https://www.pornwhite.com','https://www.pornhd.com','https://www.royal02.me','https://www.porntube.com','https://www.pervclips.com','http://uqa56.com','https://www.race55.xyz','http://sgh56.com','https://www.sexking1.site','https://www.sexbam9.me','https://www.totobank.me','https://www.sexbam10.me','https://www.torrentgirl3.com','http://nb-rf.com','https://www.slutroulette.com','https://sites.google.com','http://bmc-11.com','http://qsz43.com','https://www.wetube.xyz','https://www.youav.com','https://www.xpervs.com','https://www.yhzt02.me','https://www.torrentkim4.com','https://www.yabam1.me','https://www.xvideos.com','https://www.xnxx.com','https://xn--hy1b45cb0i13x.com','https://xn--910b67oikv.com','https://xn--6i0bp8g875a.com','https://xn--69-pw1j.com','https://xhamster.com','https://xart.letfap.com','http://zxs43.com','https://www1.ttobogo.net','https://yaburi03.com','https://xn--qh3bz6ge5a.com','https://xn--sm2bt18bbya.site','https://yadongtheater.com','http://xn--1-246fr72a.com','https://youonlywatch03.com','https://yumi16.com','https://yahun05.com','http://oneshot011.com','https://bbcp9410.com','http://bdk820.com','https://xn--hz7ba.xn--3e0b707e','https://xn--2o2bi68b94b.com']
        #self.dbConnectStore = initialize_database2('test5.db') # 결과물 DB 저장 초기화
        #self.dbBannerSites = initialize_database3('sites_banner_count.db') # 결과물 DB 저장 초기화
        self.log = open('self.log.write_log.txt','w')
        self.mainIPs = []
        self.resultUrls = []
        self.repUrls = []
        self.tmpDir = 'tmpimage'
        self.driver='.\\drivers\\chromedriver.exe'
        self.linkCount = 0
        self.header = {
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
                'Sec-Fetch-User': '?1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
                'referer' : 'https://www.google.com',
                }

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('window-size=1920x1080')
        self.options.add_argument("disable-gpu")
        self.options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self.options.add_argument("lang=ko_KR")

        os.makedirs(self.tmpDir, exist_ok=True)
    '''
    def start_requests(self):
        yield scrapy.Request(url, callback= self.link_parse, dont_filter = True, headers=self.header)
    '''
    def parse(self, response):
        items = CrawlerItem()
        baseIP = get_ip(response.url)
        #self.log.write(f'[+] mainIPs : {len(self.mainIPs)}')
        # ToDO : country = #GeoIp를 이용한 IP 구분(나라별)
        if baseIP not in self.mainIPs:
            self.mainIPs.append(baseIP)
            self.log.write(str(response.url)+" "+str(baseIP))
            print(str(response.url)+" "+str(baseIP))
            ######################################################################################################################################################
            # Stage 1. Get Url in Image having a href tag
            ######################################################################################################################################################
            images = response.css('a[href] > img') # a 태그 하이퍼 링크 있는 이미지 
            links = []
            #self.log.write("[+] test image count : %d " % len(images))
            for im_index, image in enumerate(images):
                imageSrc = image.css('img::attr(src)').get()
                dynamicFlag = False
                keyFlag = False
                if imageSrc.startswith('http'):
                    imageUrl = imageSrc
                else:
                    imageUrl = response.urljoin(imageSrc) #a 태그 하이퍼 링크 -> 이미지 링크
                
                herfLink = image.xpath('..').css('a::attr(href)').re(r'http.*') # 이지미링크에 연결된 하이퍼링크
                if len(herfLink) is 0 or (get_ip(herfLink[0]) == baseIP): # href link에 php나 javascript 단어가 있다면 selenium을 이용한 추출
                    herfLink = image.xpath('..').css('a::attr(href)').re(r'.*\.php.*|.*javascript.*|.*\.js.*')
                    if len(herfLink) is not 0:
                        herfLink = herfLink[0]
                        self.log.write(f"[+] no http : {herfLink} {response.url} {image.xpath('..').css('a::attr(href)').get()}")
                        dynamicFlag = True
                    else:
                        herfLink = None
                else:
                    herfLink = herfLink[0]
                    self.log.write(f"[+] http : {herfLink} {response.url} {image.xpath('..').css('a::attr(href)').get()}")
                ######################################################################################################################################################
                # Stage 2. Text OCR in Image file
                ######################################################################################################################################################
                text = ''
                if imageUrl.endswith('gif'): #gif의 경우 여러장의 이미지에서 텍스트 추출
                    index = 1
                    try:
                        imageBytes = requests.get(imageUrl,stream=True)
                        imageBytes.raw.decode_content = True
                        im = Image.open(imageBytes.raw)
                    except Exception as e1:
                        self.log.write("[-] image extract fail : " + str(e1))
                        try:
                            im = Image.open(urlopen(imageUrl))
                        except Exception as e2:
                            self.log.write("[-] image extract all fail : " + str(e2))
                            self.log.write("[-] image url " + imageUrl)
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
                        self.log.write("[-] image extract fail : " + str(e3))
                        self.log.write("[-] extracted text : " + text)
                        if len(text) == 0:
                            continue
                else:
                    text = detect_text_uri(imageUrl)
                text = text.upper()
                #self.log.write(f"[+] image parsing done {text} {len(text)} {dynamicFlag} {image.xpath('..').css('a::attr(href)').get()}")
                keyData = ''
                if any(word in text for word in keywords): # 추출된 텍스트에 keyword 하나라도 있으면 배너이미지로 인식
                    words = [word for word in keywords if word in text]
                    keyData = '+'.join(words)
                    keyFlag = True
  
                if keyFlag and dynamicFlag:# keyData가 있으나 hreflink를 추출하지 못한 경우 php나 javascript를 통한 링크추출
                    #javascript 등을 통해 연결되는 경우, 주소가 코드에 적혀있지 않을경우 수집 방법 -> selenium 사용하여 클릭 후 주소 획득(속도??)
                    #개발자도구 - 네트워크 - xhr 파일을 보면 json형태로 javascript:void(0)로 연결되는 주소가 적혀있는 경우가 있음
                    self.log.write(f"[+] selenium parsing start {response.url}")
                    driver = webdriver.Chrome(self.driver,options=self.options)
                    driver.implicitly_wait(10)
                    driver.get(url=response.url)
                    imageList = driver.find_elements_by_css_selector('a[href] > img')
                    imageList[im_index].find_element_by_xpath('..').click()
                    driver.switch_to.window(driver.window_handles[-1]) # 클릭한 페이지로 이동(tab switch)
                    herfLink = driver.current_url
                    driver.quit()
                    self.log.write(f"[+] dynamic extract : {herfLink}")
                
                if get_ip(herfLink) == baseIP:
                    continue
                if herfLink and keyFlag:
                    self.log.write(f'[+] append link : {herfLink} {keyData}')
                    links.append((imageUrl,herfLink,keyData))
            self.log.write(f'[+] links : {len(links)}')
            if len(links) == 0:
                items['main_url'] = urlparse(response.url).scheme + "://"+ urlparse(response.url).netloc
                items['main_ip'] = baseIP
                items['connect_url'] = 'None'
                items['connect_ip'] = 'None'
                items['keywords'] = 'None'
                items['banner_count'] = 0
                yield items
            ######################################################################################################################################################
            # Stage 3. Information Save in DB
            # Stage 4. Next Site Crawling
            ######################################################################################################################################################
            imageUrls = []
            bannerCount = len(links)
            #self.log.write(f'[+] link count : {len(links)}')
            for index, link in enumerate(links):
                ip = get_ip(link[1]) #하이퍼링크
                items['main_url'] = urlparse(response.url).scheme + "://" + urlparse(response.url).netloc
                items['main_ip'] = baseIP
                items['connect_url'] = urlparse(link[1]).scheme + "://" + urlparse(link[1]).netloc
                items['connect_ip'] = ip
                items['keywords'] = link[2]
                items['banner_count'] = bannerCount
                yield items
                imageUrls.append(link[0])
                self.log.write(f"[+] trace on : {link[1]}")
                yield scrapy.Request(link[1], callback=self.link_parse, dont_filter = True, headers=self.header)
            '''
            yield {
                'image_urls' : imageUrls
            }
            '''
        else: 
            self.log.write(f"[-] already {response.url} {baseIP} in main ip list ")

        return

    def link_parse(self, response):
        items = CrawlerItem()
        baseIP = get_ip(response.url)
        #self.log.write(f'[+] mainIPs : {len(self.mainIPs)}')
        # ToDO : country = #GeoIp를 이용한 IP 구분(나라별)
        if baseIP not in self.mainIPs:
            self.mainIPs.append(baseIP)
            self.log.write(response.url, baseIP)
            ######################################################################################################################################################
            # Stage 1. Get Url in Image having a href tag
            ######################################################################################################################################################
            images = response.css('a[href] > img') # a 태그 하이퍼 링크 있는 이미지 
            links = []
            #self.log.write("[+] test image count : %d " % len(images))
            for im_index, image in enumerate(images):
                imageSrc = image.css('img::attr(src)').get()
                dynamicFlag = False
                keyFlag = False
                if imageSrc.startswith('http'):
                    imageUrl = imageSrc
                else:
                    imageUrl = response.urljoin(imageSrc) #a 태그 하이퍼 링크 -> 이미지 링크
                
                herfLink = image.xpath('..').css('a::attr(href)').re(r'http.*') # 이지미링크에 연결된 하이퍼링크
                if len(herfLink) is 0 or (get_ip(herfLink[0]) == baseIP): # href link에 php나 javascript 단어가 있다면 selenium을 이용한 추출
                    herfLink = image.xpath('..').css('a::attr(href)').re(r'.*\.php.*|.*javascript.*|.*\.js.*')
                    if len(herfLink) is not 0:
                        herfLink = herfLink[0]
                        self.log.write(f"[+] no http : {herfLink} {response.url} {image.xpath('..').css('a::attr(href)').get()}")
                        dynamicFlag = True
                    else:
                        herfLink = None
                else:
                    herfLink = herfLink[0]
                    self.log.write(f"[+] http : {herfLink} {response.url} {image.xpath('..').css('a::attr(href)').get()}")
                ######################################################################################################################################################
                # Stage 2. Text OCR in Image file
                ######################################################################################################################################################
                text = ''
                if imageUrl.endswith('gif'): #gif의 경우 여러장의 이미지에서 텍스트 추출
                    index = 1
                    try:
                        imageBytes = requests.get(imageUrl,stream=True)
                        imageBytes.raw.decode_content = True
                        im = Image.open(imageBytes.raw)
                    except Exception as e1:
                        self.log.write("[-] image extract fail : " + str(e1))
                        try:
                            im = Image.open(urlopen(imageUrl))
                        except Exception as e2:
                            self.log.write("[-] image extract all fail : " + str(e2))
                            self.log.write("[-] image url " + imageUrl)
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
                        self.log.write("[-] image extract fail : " + str(e3))
                        self.log.write("[-] extracted text : " + text)
                        if len(text) == 0:
                            continue
                else:
                    text = detect_text_uri(imageUrl)
                text = text.upper()
                #self.log.write(f"[+] image parsing done {text} {len(text)} {dynamicFlag} {image.xpath('..').css('a::attr(href)').get()}")
                keyData = ''
                if any(word in text for word in keywords): # 추출된 텍스트에 keyword 하나라도 있으면 배너이미지로 인식
                    words = [word for word in keywords if word in text]
                    keyData = '+'.join(words)
                    keyFlag = True
  
                if keyFlag and dynamicFlag:# keyData가 있으나 hreflink를 추출하지 못한 경우 php나 javascript를 통한 링크추출
                    #javascript 등을 통해 연결되는 경우, 주소가 코드에 적혀있지 않을경우 수집 방법 -> selenium 사용하여 클릭 후 주소 획득(속도??)
                    #개발자도구 - 네트워크 - xhr 파일을 보면 json형태로 javascript:void(0)로 연결되는 주소가 적혀있는 경우가 있음
                    self.log.write(f"[+] selenium parsing start {response.url}")
                    driver = webdriver.Chrome(self.driver,options=self.options)
                    driver.implicitly_wait(10)
                    driver.get(url=response.url)
                    imageList = driver.find_elements_by_css_selector('a[href] > img')
                    imageList[im_index].find_element_by_xpath('..').click()
                    driver.switch_to.window(driver.window_handles[-1]) # 클릭한 페이지로 이동(tab switch)
                    herfLink = driver.current_url
                    driver.quit()
                    self.log.write(f"[+] dynamic extract : {herfLink}")
                
                if get_ip(herfLink) == baseIP:
                    continue
                if herfLink and keyFlag:
                    self.log.write(f'[+] append link : {herfLink} {keyData}')
                    links.append((imageUrl,herfLink,keyData))
            self.log.write(f'[+] links : {len(links)}')
            if len(links) == 0:
                items['main_url'] = urlparse(response.url).scheme + "://"+ urlparse(response.url).netloc
                items['main_ip'] = baseIP
                items['connect_url'] = 'None'
                items['connect_ip'] = 'None'
                items['keywords'] = 'None'
                items['banner_count'] = 0
                yield items
            ######################################################################################################################################################
            # Stage 3. Information Save in DB
            # Stage 4. Next Site Crawling
            ######################################################################################################################################################
            imageUrls = []
            bannerCount = len(links)
            #self.log.write(f'[+] link count : {len(links)}')
            for index, link in enumerate(links):
                ip = get_ip(link[1]) #하이퍼링크
                items['main_url'] = urlparse(response.url).scheme + "://" + urlparse(response.url).netloc
                items['main_ip'] = baseIP
                items['connect_url'] = urlparse(link[1]).scheme + "://" + urlparse(link[1]).netloc
                items['connect_ip'] = ip
                items['keywords'] = link[2]
                items['banner_count'] = bannerCount
                yield items
                imageUrls.append(link[0])
                self.log.write(f"[+] trace on : {link[1]}")
                yield scrapy.Request(link[1], callback=self.link_parse, dont_filter = True, headers=self.header)
            '''
            yield {
                'image_urls' : imageUrls
            }
            '''
        else: 
            self.log.write(f"[-] already {response.url} {baseIP} in main ip list ")

        return

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
                self.log.write(e)
        return True if len(result.fetchall()) > 0 else False
