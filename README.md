# CrawlProject
Korea Univ Paper Crawler Project

# Usage
Scrapy 모듈을 사용한 크롤러 작성
## Environment
```
python 3.7.8
```
## Stage
```
1) install pip
2) command : pip install pip env (with powershell)
3) git clone this project
4) command : pipenv run(in project folder)
5) command : pipenv install(install packages)
6) command : scrapy sites --nolog (sites is spider name)
```
* illegals.db is first db for get connection sites
* sites_connection.db is result db from scrapy crawler
* 현재는 해당 메인페이지에서 해당사이트와 다른 IP로 접근하는 URL, IP 수집(전체 태그 중 href에 http가 포함되는 링크 수집 후 IP 비교)

# TODO
```
banner selector, recursive site trace, (option) items.py setting
```