from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.binary_location = '/usr/bin/opera' #ブラウザはOperaを使用

def horse_list(url):

    options.add_argument('--headless')  # ヘッドレスモードで起動
    options.add_argument('--disable-gpu')  # GPUの無効化
    options.add_argument('--no-sandbox')  # サンドボックスモードの無効化
    options.add_argument('--disable-dev-shm-usage')  # 共有メモリの無効化

    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)
    
    try:
        # driver.request_interceptor = interceptor
        driver.get(url) #Too slow
        driver.implicitly_wait(10)

        html = driver.page_source
    finally:
        driver.quit()

    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(html, 'html.parser')

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
