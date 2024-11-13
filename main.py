# Pythonライブラリ
import logging
import google.cloud.logging
from fastapi import FastAPI, Request
import json
# .pyライブラリ
from lib.airwork import AirWork
from lib.engage import Engage

app = FastAPI()

# Cloud Loggingハンドラを標準loggingモジュールに接続する
log_client = google.cloud.logging.Client()
log_client.setup_logging()

# ロガーを取得
logger = logging.getLogger(__name__)

# エンドポイントの動作
@app.post("/")
async def search_endpoint(request: Request):
    # リクエストの受信をログに記録
    logger.info("リクエストを受信しました")
    try:
        # JSONデータの取得と解析
        json_data = await request.json()
        json_message = GetJson(json_data)        
        logger.debug("プログラムは終了しました。")
        return json_message
    except Exception as e:
        # 例外発生時のエラーログ記録
        logger.error("エラー発生", exc_info=True)
        return {"result": "GetJson()は動作していません。"}
    

# プログラミングの呼び出し
def GetJson(json_data):
    data = json.loads(json_data)
    message = {"result" : "初期化"}
    json_message = {"result" : "初期化"}
    if data['run_mode'] == 'update':
        if data['target_site'] == 'airwork':
            instance = AirWork(data)
            message = instance.AirworkUpdate()
            json_message = json.dumps(message)
            return json_message
        elif data['target_site'] == 'engage':
            instance = Engage(data)
            message = instance.EngageUpdate()
            json_message = json.dumps(message)
            return json_message
        else:
            message = {"result" : "ターゲットサイトが指定されていません。"}
            json_message = json.dumps(message)
            return json_message
    elif data['run_mode'] == 'scout':
        if data['target_site'] == 'airwork':
            # instance = AirWork(data)
            # message = instance.AirWorkScount()
            message = {"result" : "実装中です。"}
            json_message = json.dumps(message)
            return json_message
        elif data['target_site'] == 'engage':
            # instance = Engage(data)
            # message = instance.EngageScount()
            message = {"result" : "実装中です。"}
            json_message = json.dumps(message)
            return json_message
        else:
            message = {"result" : "ターゲットサイトが指定されていません。"}
            json_message = json.dumps(message)
            return json_message
    else:
        message = {"result" : "動作モードが指定されていません。"}
        json_message = json.dumps(message)
        return json_message






