import requests,bs4
from rich import print,logging,pretty,inspect
from rich.console import Console
import re
from pydantic import BaseModel
from typing import List

console = Console()
pretty.install()


class RaceInfo(BaseModel):
    race_num:str
    race_name:str
    race_class:str
    race_dist:str
    race_type:str
    race_time:str
    link:str
class RacePlaceInfo(BaseModel):
    race_place:str
    race_info_list:List[RaceInfo] = []
class RaceAssociationInfo(BaseModel):
    association:str
    race_place_info_list:List[RacePlaceInfo] = []
race_place_id_dict = {
    "札幌":1,
    "函館":2,
    "福島":3,
    "新潟":4,
    "東京":5,
    "中山":6,
    "中京":7,
    "京都":8,
    "阪神":9,
    "小倉":10,
    "門別":30,
    "帯広ば":65,
    "盛岡":35,
    "水沢":36,
    "大井":44,
    "金沢":46,
    "名古屋":48,
    "佐賀":55,
    "浦和":42,
    "笠松":47,
    "船橋":43,
    "川崎":45,
    "園田":50,
    "姫路":51,
    "高知":54
}

def getRaceID(race_place_info,race_num,year):
    open_num = race_place_info.race_place.split("回")[0]
    race_place = re.split("\d+",race_place_info.race_place.split("回")[1])[0]
    open_day = race_place_info.race_place.split(race_place)[1].replace("日","").replace("回","")
    race_place_id = race_place_id_dict[race_place]
    race_id = f"{year}{str(race_place_id).zfill(2)}{open_num.zfill(2)}{open_day.zfill(2)}{race_num.zfill(2)}"
    return race_id

def getRaceIDNar(race_place,race_num,year,month,day):
    race_place_id = race_place_id_dict[race_place]
    race_id = f"{year}{str(race_place_id).zfill(2)}{month.zfill(2)}{day.zfill(2)}{race_num.zfill(2)}"
    return race_id

def getRaceInfo(date:str) -> RaceAssociationInfo:
    date = date.split("/")
    #中央レース情報を取得する
    url = f"https://www.jra.go.jp/keiba/calendar{date[0]}/{date[0]}/{str(int(date[1]))}/{''.join(date[-2:])}.html"
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.content, 'html.parser')
    race_place_list = soup.find_all(class_ = "mt20",id = "program_list")
    race_place_list = race_place_list[0].find_all(class_ = "cell")
    
    race_association_info = RaceAssociationInfo(association = "中央")
    for race_place in race_place_list:
        if race_place.text == "":
            continue
        race_place_text = race_place.find_all(class_ = "main")[0].text
        race_place_info = RacePlaceInfo(race_place=race_place_text)
        #console.log(race_place_info)
        race_list = race_place.find_all("tr")
        for race in race_list[1:]:
            race_num = race.find_all(class_ = "num")[0].text
            race_name = race.find_all(class_ = "stakes")
            if race_name == []:
                race_name = ""
            else:
                race_name = race_name[0].text
            race_name = race_name
            race_class = race.find_all(class_ = "race_class")[0].text
            race_dist = race.find_all(class_ = "dist")[0].text
            race_type = race.find_all(class_ = "type")[0].text
            race_time = race.find_all(class_ = "time")[0].text
            race_id = getRaceID(race_place_info,race_num.replace("レース",""),date[0])
            link = f"https://race.netkeiba.com/race/result.html?race_id={race_id}"
            race_info = RaceInfo(
                race_num=race_num,
                race_name=race_name,
                race_class=race_class,
                race_dist=race_dist,
                race_type=race_type,
                race_time=race_time,
                link=link
            )
            race_place_info.race_info_list.append(race_info)
            #console.log(race_num,race_name,race_class,race_dist,race_type)
        race_association_info.race_place_info_list.append(race_place_info)
    #console.log(race_info_text)
    return race_association_info

def getRaceInfoNar(date:str) -> RaceAssociationInfo:
    date = date.split("/")
    #地方レース情報を取得する
    url = f"https://www.keiba.go.jp/KeibaWeb/MonthlyConveneInfo/MonthlyConveneInfoTop?k_year={date[0]}&k_month={str(int(date[1]))}"
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.content, 'html.parser')
    race_place_list = soup.find_all(class_ = "schedule")[0].find_all("tr")[2:]
    day = int(date[-1])
    
    race_association_info = RaceAssociationInfo(association = "地方")
    for race_place in race_place_list:
        if race_place.find_all("td")[day].text.replace("\n","") != "":
            race_place_name = race_place.find_all("td")[0].text
            race_info_link = race_place.find_all("td")[day].contents[1].attrs["href"]
            html = requests.get("https://www.keiba.go.jp"+race_info_link)
            soup = bs4.BeautifulSoup(html.content, 'html.parser')
            race_list = soup.find_all("table")[0].find_all(class_ = "data")
            
            race_place_info = RacePlaceInfo(race_place=race_place_name)
            for race in race_list:
                race_num = race.find_all("td")[0].text.replace("R","レース")
                race_time = "{}時{}分".format(*race.find_all("td")[1].text.split(":"))
                race_name = race.find_all("td")[4].text.replace("\n","")
                race_dist = race.find_all("td")[5].text
                race_id = getRaceIDNar(race_place_name,race_num.replace("レース",""),date[0],date[1],date[2])
                link = f"https://nar.netkeiba.com/race/result.html?race_id={race_id}"
                
                race_info = RaceInfo(
                    race_num=race_num,
                    race_name=race_name,
                    race_class="",
                    race_dist=race_dist,
                    race_type="",
                    race_time=race_time,
                    link=link
                )
                race_place_info.race_info_list.append(race_info)
            
            race_association_info.race_place_info_list.append(race_place_info)
    
    return race_association_info

if __name__ == "__main__":
    print(getRaceInfo("2023/08/06"))
    print(getRaceInfoNar("2023/08/06"))
