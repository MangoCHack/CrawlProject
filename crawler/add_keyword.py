
import pandas as pd

site_type = {
    '도박' : ['코드', '가입', '카지노', '스포츠', '고액', '상한', '놀이터', '해외', '배당', '가입코드', '문의', '안전', '업체', '지급', '배팅', '보증',\
            '포커', '경기', '미니', '천만원고액전용', '환전', '미니게임', '스포츠상한', '매출', '인플레이', '이벤트', '천만', '게임', '라이브포커', '호텔카지노',\
            '파트너', '베팅', '머니', '유럽식스포츠', '보너스', '시간', '쿠폰', '제한', '토토', '파워볼', 'CASINO', 'GASINO', 'SPIN', '도박', '수익', '당일',\
            '가입머니', '슬롯', 'SPORT', '이터', '노리', '메이저', '국내배당' , '배팅가능' ,'오버가능' , '보증업체', '놀이터코드' , '무제한', 'BET', '실시간',\
            '신규가입', '입금', '각종문의', '먹튀', '회원', '바카라', '먹튀검증', '전용', '호텔', '고객', '크로스', '예치', '상한가', '보증금', '시청' ],
    '성인용품' : ['성인', '상품', '용품', '판매', '배송', '리얼', '오르가즘', '포인트', '리얼돌', '바나나몰', '총판문의'],
    '약물' : ['상품', '비아그라', '판매', '배송', 'DRUG', '마약', '총판문의'],
    '저작물' : ['영화', '드라마', '제휴', '웹툰', '토렌트', '시리즈', 'TORRENT', '애니', '중계', '링크', '총집합' ],
    '성인물' : ['라이브', '명기', '토렌트', '야동', '시리즈', '리얼', '오르가즘', '다운로드', '티비', '영상', '총판', '방송', '총집합'],
    '불법업소' : ['업소'],
    '불법기타' : ['증명', '광고', '텔레그램']
}

fp = open('final.csv','r', encoding='utf-8')
lines = fp.readlines()
fp.close()
del lines[0]

connect_urls = {}
for l in lines:
    values = l.strip().split(',')
    connect_url = values[2].strip('/')
    if connect_url in connect_urls.keys():
        continue
    connect_urls[connect_url] = {'도박':0,'성인용품':0,'약물':0,'저작물':0,'성인물':0,'불법업소':0,'불법기타':0}

for l in lines:
    values = l.strip().split(',')
    connect_url = values[2].strip('/')
    keyword = values[4]
    keywords = keyword.split('+')
    for k in keywords:
        for t in site_type:
            if k in site_type[t]:
                connect_urls[connect_url][t] += 1

fp2 = open('result.csv','w')
fp2.write('main_url,main_ip,connect_url,connect_ip,keywords,banner_count,site_type\n')
for l in lines:
    values = l.strip().split(',')
    main_url = values[0].strip('/')
    if main_url in connect_urls.keys():
        _type = max(connect_urls[main_url],key=connect_urls[main_url].get)
        l = l.strip()+','+_type+'\n'
        fp2.write(l)
    else:
        l = l.strip()+','+'None'+'\n'
        fp2.write(l)

fp2.close()