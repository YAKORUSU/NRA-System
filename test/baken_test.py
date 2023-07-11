from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from rich import print, pretty
from rich.console import Console

console = Console()
pretty.install()
# chromedriverのパスを指定
executable_path = "./chromedriver.exe"

options = Options()
options.add_argument('--headless')  # ヘッドレスモードで起動
options.add_argument('--disable-gpu')  # GPUの無効化
options.add_argument('--no-sandbox')  # サンドボックスモードの無効化
options.add_argument('--disable-dev-shm-usage')  # 共有メモリの無効化


def horse_list(url):
    # WebDriverの初期化
    with webdriver.Chrome(executable_path=executable_path, options=options) as driver:
            # URLをブロック（定義したURLをブロックする）
        driver.execute_cdp_cmd('Network.setBlockedURLs', {
            'urls': [
                #ここにブロックするURLを追加
                'https://ads.stickyadstv.com/',
                'https://c.amazon-adsystem.com/',
                'https://images.taboola.com/',
                'https://imageproxy.as.criteo.net/',
                'https://hk-wf.taboola.com/',
                'https://gum.criteo.com/',
                'https://s.adroll.com/',
                'https://s0.2mdn.net',

            ]})

        # HTMLを取得
        driver.get(url)
        html = driver.page_source

    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(html, 'html.parser', from_encoding='UTF-8')

    # レースIDを取得
    race_id = url.split('=')[1]

    # 表のデータを抽出してJson形式に整形
    table = soup.find('tbody')
    rows = table.find_all('tr', class_='HorseList')
    result = {
        'raceid': race_id,
        'main': {}
    }
    for row in rows:
        columns = row.find_all('td')
        number = columns[1].text.strip()
        horse_name = columns[3].text.strip()
        frame = int(columns[0].text.strip())
        odds = float(columns[9].text.strip())
        ninki = int(columns[10].text.strip())

        result['main'][number] = {
            '馬名': horse_name,
            '枠': frame,
            'オッズ': odds,
            '人気': ninki
        }

    response_json = f'{result}'

    return response_json



# テスト実行
url = 'https://race.netkeiba.com/race/shutuba.html?race_id=202303020611'
race_result = horse_list(url)
print(race_result)
