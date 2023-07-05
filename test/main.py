#webサーバーを作成する
from fastapi import FastAPI
from fastapi.responses import FileResponse
import azure.cognitiveservices.speech as speechsdk
import urllib.parse
import tempfile
import os


app = FastAPI()

@app.get("/synthesize/{textrequest}")
async def synthesize_text(textrequest:str):
    
    # リクエストのデータをTextRequestオブジェクトに変換
    text_request = urllib.parse.unquote(f"{textrequest}")
    # return text_request
    print(text_request)
    # Azure Cognitive Services Speech SDKの設定
    speech_key = "278f4ba6837b4a299ab3502f778bf07d"
    service_region = "eastasia"
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    # テキストをwavに変換
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name='ja-JP-AoiNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(text_request).get()

    # 音声を取得
    audio_data = result.audio_data

    # 音声を一時ファイルに保存
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write(audio_data)
    
    # wavファイルをリターン
    response = FileResponse(temp_filename)

    # レスポンスを返した後に一時ファイルを削除
    @response.on_event("after_send")
    async def delete_temp_file():
        os.remove(temp_filename)

    return response    



