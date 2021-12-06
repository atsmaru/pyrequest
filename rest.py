# 準備：ライブラリのimport と 定数読み込み
import configparser
import requests
import json
import re

import base64
import os
from datetime import datetime

'''
url1 = "http://zip.cgis.biz/xml/zip.php"
payload = {"zn": "1310045"}
r = requests.get(url1, params=payload)
print(r.text)
'''

config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')
URL = config_ini['DEFAULT']['URL']
USER = config_ini['DEFAULT']['USER']
PW = config_ini['DEFAULT']['PW']


# BASIC認証方式で認証を通す:
# https://qiita.com/atmaru/items/1f66d20a16657e493ccd
#url = "https://qiita.com/api/v2/items/1f66d20a16657e493ccd/likes"
#url = "https://qiita.com/api/v2/tags"
#url = "https://qiita.com/api/v2/users/atmaru/following_tags"
#r = requests.get(url, auth=("atsmaru@gmail.com", "aki140Qi"))
#r = requests.get(url, auth=("atmaru", "aki140Qi"))


def GetRequest(command):
    res = requests.get(URL+command)
    return res

if __name__=='__main__':

    res = GetRequest("users/atmaru/following_tags")
    if res.status_code == 200:
        json_obj = res.json()
        print(json.dumps(json_obj, indent=4))
        #param = json.loads(res.json())
        #print(param)
        print('json_obj:{}'.format(type(json_obj)))
        #print(json_obj)

        for list in json_obj:
            #print(list)
            #print('items_count' in list)
            print("items_count", list['items_count'])

        # ★ポイント3    
        #fileName = json_obj['fileName']
        #contentType = json_obj['contentType']
        #contentDataAscii = json_obj['contentData']

        # ★ポイント4
        #contentData = base64.b64decode(contentDataAscii)

        #DOWNLOAD_SAVE_DIR = os.getenv("DOWNLOAD_SAVE_DIR")
        DOWNLOAD_SAVE_DIR = "c:/temp/"
        fileName = "download.json"
        contentData = json.dumps(json_obj, indent=4)

        # ★ポイント5
        saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") + fileName
        saveFilePath = os.path.join(DOWNLOAD_SAVE_DIR, saveFileName)
        with open(saveFilePath, 'wb') as saveFile:
            saveFile.write(contentData)

    else:
        print('接続失敗(><)', res.status_code)
