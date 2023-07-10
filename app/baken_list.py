from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from rich import print,pretty
from rich.console import Console

console = Console()
pretty.install()
#chomedriverのパスを指定
executable_path="./chromedriver.exe"

result_raceID_list = []
done_raceID_list = []
result_raceID_dict = {}
options = Options()
options.add_argument('--headless')

def horse_list(url):
    # HTMLを取得
    driver = webdriver.Chrome(executable_path=executable_path, options=options)
    driver.get(url)
    html = driver.page_source

    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(html, 'html.parser', from_encoding='UTF-8')

    # レースIDを取得
    race_id = url.split('=')[1]

    # 表のデータを抽出してJson形式に整形
    table = soup.find('tbody')
    rows = table.find_all('tr', class_='HorseList') # ヘッダー行を除外
    result = {}
    result['raceid'] = race_id
    result['main'] = []
    for row in rows:
        columns = row.find_all('td')
        number = columns[1].text.strip()
        horse_name = columns[3].text.strip()
        frame = int(columns[0].text.strip())
        odds = float(columns[9].text.strip())
      　ninki = int(columns[10].text.sprip())

        result['main'][number] = {
            '馬名': horse_name,
            '枠': frame,
            'オッズ': odds,
            '人気': ninki          
        }

    response_json = f"{result}"
    return response_json
