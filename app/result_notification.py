# Purpose: 結果通知を行う
# uvicorn result_notification:app --reloadをGunicornにてデーモンで起動する
#　起動コマンド: sudo systemctl start gunicorn.service

from rich import pretty
from rich.console import Console
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocket
from pydantic import BaseModel
from fastapi.responses import FileResponse
import azure.cognitiveservices.speech as speechsdk

import format_result_nar_race
import format_result_race
import baken_list

import getRaceInfo
import urllib.parse
import tempfile
import os


console = Console()
pretty.install()

"""
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger("rich")
"""

# FastAPIのインスタンスを作成
app = FastAPI()

class TextRequest(BaseModel):
    text: str

# websocketで接続中のクライアントを識別するためのIDを格納
clients = {}


# 接続確認用のエンドポイント
@app.get("/")
async def read():
    return {"Result": "ok"}

# レース結果を取得するエンドポイント
@app.get("/nar_result_info/{race_id}") #race_idはレースID
async def result_info(race_id:str):
    url = f"https://nar.netkeiba.com/race/result.html?race_id={race_id}"
    # 使用する変換スクリプト{format_result_nar_race.py}
    return format_result_nar_race.get_race_result(url)

# レース結果を取得するエンドポイント
@app.get("/result_info/{race_id}") #race_idはレースID
async def result_info(race_id:str):
    url = f"https://race.netkeiba.com/race/result.html?race_id={race_id}"
    # 使用する変換スクリプト｛format_result_race.py}
    return format_result_race.get_race_result(url)

# 開催されるレースの一覧を取得するエンドポイント
@app.get("/race_list/{date}")
async def result_info(date:str):
    try:
        date = f"{date[:4]}/{date[4:6]}/{date[6:]}"
        race_list = getRaceInfo.getRaceInfo(date)
    except:
        return "error"
    return race_list
    # return date

# 開催されるレースの一覧を取得するエンドポイント
@app.get("/nar_race_list/{date}")
async def result_info(date:str):
    try:
        date = f"{date[:4]}/{date[4:6]}/{date[6:]}"
        race_list = getRaceInfo.getRaceInfoNar(date)
    except:
        return "error"
    return race_list

@app.get("/baken/{race_id}") #race_idはレースID
async def result_info(race_id:str):
    url = f"https://race.netkeiba.com/race/shutuba.html?race_id={race_id}"
    # 使用する変換スクリプト｛baken_list.py}
    return baken_list.horse_list(url)

@app.get("/nar_baken/{race_id}") #race_idはレースID
async def result_info(race_id:str):
    url = f"https://nar.netkeiba.com/race/shutuba.html?race_id={race_id}"
    # 使用する変換スクリプト｛baken_list.py}
    return baken_list.horse_list(url)

@app.get("/synthesize/{textrequest}")
async def synthesize_text(textrequest:str):

    # リクエストのデータをTextRequestオブジェクトに変換
    text_request = urllib.parse.unquote(f"{textrequest}")
    # return text_request
    print(text_request)

    #リクエストが来たら/tmp内の.wavファイルを全部削除する
    for file in os.listdir("/tmp"):
        if file.endswith(".wav"):
            os.remove(os.path.join("/tmp", file))
            
    # Azure Cognitive Services Speech SDKの設定
    speech_key = "{API_key}"
    service_region = "japanwest"
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    # テキストをwavに変換
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name='ja-JP-NanamiNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text_request).get()

# 音声を取得
    audio_data = result.audio_data

    # 音声を一時ファイルに保存
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write(audio_data)

    # wavファイルをリターン
    return FileResponse(temp_filename)

# websocketで接続中のクライアントにレース結果をリアルタイム送信するエンドポイント
@app.websocket("/ws/result")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    
    try:
        text = await ws.receive_text()
        console.log(text)
        for client in clients.values():
            await client.send_text(text)
    except Exception as e:
        console.log("LOG_DEBUG", '{}:{}'.format(type(e),e))
        ws.close()

# websocketで接続中のクライアントにメッセージ送信するエンドポイント
@app.websocket("/ws/connection")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    # クライアントを識別するためのIDを取得
    key = ws.headers.get('sec-websocket-key')
    clients[key] = ws
    
    try:
        while True:
            data = await ws.receive_text()
    except:
        #await ws.close()
        # 接続が切れた場合、当該クライアントを削除する
        del clients[key]

