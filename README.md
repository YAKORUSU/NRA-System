# NRJ-System
Neos競馬場関連システムの統合管理

## ファイルの内容
- app
  - レース結果通知用アプリケーション
 
## 動作環境
- Chrome

 Install using `wget`&`apt`:
```shell
# リポジトリ追加
$ sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# 公開鍵のダウンロードと登録
$ sudo wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# インストール
$ sudo apt update
$ sudo apt install google-chrome-stable

# インストール＆バージョン確認
$ google-chrome --version
Google Chrome 86.0.4240.75
```
- ChromeDriver

Python3-Seleniumをダウンロードすると一緒にインストールされる

バージョン確認
```Shell
#バージョンがChromeバージョンと一致していることを確認する
$ chromedriver -v
ChromeDriver 85.0.4183.121 (a81aa729a8e1fd413943a339393c82e7b8055ddc-refs/branch-heads/4183@{#1864})
```
一致していれば現状のままでOK

※一致していない場合の対処について
```Shell
#zipファイルを扱うためのツールをインストール
$ sudo apt install unzip
$ sudo apt install unzip zip
```
`curl`でダウンロードする
ダウンロードファイルはtmpに入れる
```Shell
$ cd /tmp/

#${ChromeVer}に前項で確認したchromeバージョンを入れる
$ curl -O https://chromedriver.storage.googleapis.com/${ChromeVer}/chromedriver_linux64.zip

#ダウンロードの確認
$ ls -l

#zipの解凍及び配置
$ unzip chromedriver_linux64.zip
$ sudo mv chromedriver /usr/local/bin/

#配置後の確認及び元ファイルの削除
$ which chromedriver 
$ rm chromedriver_linux64.zip
```