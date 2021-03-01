from selenium import webdriver
from selenium.webdriver.chrome.options import Options
 
CHROMEDRIVER_PATH = './drivers/chromedriver.exe' # Windows는 chromedriver.exe로 변경
WINDOW_SIZE = "1920,1080"
 
chrome_option = Options()
chrome_option.add_argument( "--headless" )     # 크롬창이 열리지 않음
chrome_option.add_argument( "--no-sandbox" )   # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
chrome_option.add_argument( "--disable-gpu" )  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
chrome_option.add_argument(f"--window-size={ WINDOW_SIZE }")
chrome_option.add_argument('Content-Type=application/json; charset=utf-8')
 
driver = webdriver.Chrome( executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_option )
driver.get( 'https://news.naver.com' )