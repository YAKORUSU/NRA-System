# NotificationRaceResults

## Motivation

競馬場がVRの中にあったら面白いという話が発端です。 
競馬の最新情報はネット競馬にて配信されていることがわかりました。
上記サイトから情報を抜き取りWebSocketに流すサーバがあればレース結果の通知が実現できるということがわかり作ることにしました。

## Overview

競馬レース速報をWebsocketにて接続しているクライアントに通知します。
このWebアプリでは下記の機能を提供しています。

- ネット競馬のwebページから最新のレース情報を取得するスクレイパー
- 競馬レース速報をNeosVR内から受け取るためのWebsocketのエンドポイント

## Infrastructure

### 論理構成図

// TODO

### WebAPIエンドポイント
```console
WebSocket : ws://{$HostName}:8080/ws/connection
http : http://{$HostName}:8080/　#接続確認用
```
- WebSocket : ws://{$HostName}:8000/ws/connection
- http : http://{$HostName}:8000/

### サーバ情報

- ConoHaVPS (vCPU:2,Mem:1GB)

#### webサーバ

- nginx
  - 8080にてListen

#### ASGIサーバ

- gunicorn
- uvicorn

##### プロセス管理

- systemdにてgunicornをデーモン化
- gunicornではuvicornをマルチプロセス化して起動

#### ファイアウォール

- ufwにて制御

## Application

### 技術仕様

- 言語：Pytnon3系
- フレームワーク：FastAPI

### レース結果通知フロー

// TODO

### Test

### コネクション数制限
// TODO 調整中

## About
// TODO
