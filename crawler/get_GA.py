import requests
import bs4
import re

def get_ga(url: str):
    url_with_scheme = "https://" + url if "//" not in url else url
    try:
        response = requests.get(url_with_scheme, stream=True)
        soup = bs4.BeautifulSoup(response.content, "html5lib")
    except:
        return 'None'
    else:
        google_analytics_pattern = re.compile(r"UA-[0-9]+-[0-9]+")
        google_analytics_pattern_ver4 = re.compile(r'G-\w+')

        google_analytics_codes = google_analytics_pattern.findall(
            " ".join(
                [
                    str(script_tag)
                    for script_tag in soup.find_all("script", {"src": True})
                ]
            )
        )

        google_analytics_codes_ver4 = google_analytics_pattern_ver4.findall(
            " ".join(
                [
                    str(script_tag)
                    for script_tag in soup.find_all("script", {"src": True})
                ]
            )
        )

    if len(google_analytics_codes) == 0 and len(google_analytics_codes_ver4) != 0:
        google_analytics_codes = google_analytics_codes_ver4
    elif len(google_analytics_codes) == 0 and len(google_analytics_codes_ver4) == 0:
        google_analytics_codes = ['None']
    return ' '.join(google_analytics_codes)

if __name__ == '__main__':
    fp = open('result.csv','r', encoding='cp949')
    lines = fp.readlines()
    fp.close()
    del lines[0]

    fp2 = open('result2.csv','w')
    fp2.write('main_url,main_ip,connect_url,connect_ip,keywords,banner_count,site_type,main_country,is_main_cloud,main_org,connect_country,is_connect_cloud,connect_org,main_ga,connect_ga\n')
    for l in lines:
        l = l.strip()
        values = l.split(',')
        main_url = values[0].strip('/')
        connect_url = values[2].strip('/')
        main_ga = get_ga(main_url)
        connect_ga = get_ga(connect_url)
        print(main_ga)
        print(connect_ga)

        l = l + ',' + main_ga + ',' + connect_ga + '\n'
        fp2.write(l)

    fp2.close()