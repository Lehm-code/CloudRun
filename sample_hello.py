import logging
import google.cloud.logging
from fastapi import FastAPI, Request

app = FastAPI()

# Cloud Loggingハンドラを標準loggingモジュールに接続する
log_client = google.cloud.logging.Client()
log_client.setup_logging()

# ロガーを取得
logger = logging.getLogger(__name__)

@app.post("/")
async def read_root(request: Request):
    # リクエストの受信をログに記録
    logger.info("リクエストを受信しました")
    try:
        # JSONデータの取得と解析
        data = await request.json()
        last_name = data.get("lastName")
        first_name = data.get("firstName")
        
        # デバッグ情報のログ記録
        logger.debug(f"リクエストデータ: {data}")
        
        # 名前が存在する場合の処理
        if last_name and first_name:
            message = f"Hello, {last_name} {first_name}! from Python"
            logger.info(f"返信メッセージ: {message}")
            return {"message": message}
        else:
            # 名前がない場合の処理
            logger.warning("名前が入力されていません。")
            return {"message": "Hello, World! from Python"}
    except Exception as e:
        # 例外発生時のエラーログ記録
        logger.error("エラー発生", exc_info=True)
        return {"message": "An error occurred during processing"}
