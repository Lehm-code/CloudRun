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
        data = await request.json()
        json_message = GetJson(data)        
        logger.debug("プログラムは終了しました。")
        return json_message
    except json.JSONDecodeError:
        # JSONデコードエラーのログとレスポンス
        logger.error("JSONのデコードに失敗しました。無効なJSON形式です。", exc_info=True)
        return {"result" :"無効なJSON形式です。"}
    except Exception as e:
        # 例外発生時のエラーログ記録
        logger.error("予期しないエラーが発生しました。", exc_info=True)
        return {"result" :"予期しないエラーが発生しました。"}


# プログラミングの呼び出し
def GetJson(data):
    message = {"result" : "初期化"}
    json_message = {"result" : "初期化"}
    # 必要なキーの存在確認
    if 'run_mode' not in data:
        return json.dumps({"result": "動作モードが指定されていません。"})
    if 'target_site' not in data:
        return json.dumps({"result": "ターゲットサイトが指定されていません。"})
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
            return json.dumps({"result": "ターゲットサイトが指定されていません。"})
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
            return json.dumps({"result": "ターゲットサイトが指定されていません。"})
    else:
        message = {"result" : "動作モードが指定されていません。"}
        json_message = json.dumps(message)
        return json_message






