# Neo馬券の販売システムの構築

## Motivation
NeosVRの競馬場において稼働させていた競馬システムにNeos内通貨を用いた馬券購入システムを作りたい

## Overview
出場馬及びオッズの取得を行うクライアント
上記取得情報のJson化及び送信を行うエンドポイントの提供

## リクエスト形式
```Shell
#出場馬及び単勝のオッズ取得
$ curl http://{hostname}:8081/baken/{レースID}

#Response
{
  
