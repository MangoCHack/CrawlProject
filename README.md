# CrawlProject
Korea Univ Paper Crawler Project

# Usage
Scrapy 모듈을 사용한 크롤러 작성
## Environment
```
python 3.7.8
scrapy
selenium
```
## Stage
```
1) install pip
2) command : pip install pip env (with powershell)
3) git clone [this project]
4) command : pipenv shell(in project folder)
5) command : pipenv install(install packages)
6) command : cd crawler
7) command : scrapy crawl sites --nolog (sites is spider name)
```
* illegals.db is first db for get connection sites
* sites_connection.db is result db from scrapy crawler
* 현재 해당 메인페이지에서 이미지배너 내 텍스트 추출 후 키워드 비교 후 다른 IP로 접근하는 URL, IP 수집 중(추적제한 X)
* 배너 이미지 수집(오탐 확인용)

# TODO
```
items.py setting, 동적 웹페이지 생성 및 서버로부터 호출시 주소 수집방법 찾기
```