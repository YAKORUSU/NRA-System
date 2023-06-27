# NRJ-System
Neos競馬場関連システムの統合管理

## ファイルの内容
- app
  - レース結果通知用アプリケーション
 
## 動作環境
- Chrome

```console
# リポジトリ追加
$ sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# 公開鍵のダウンロードと登録
$ sudo wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# インストール
$ sudo apt update
$ sudo apt install google-chrome-stable
