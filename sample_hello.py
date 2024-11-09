import logging
from fastapi import FastAPI, Request

app = FastAPI()

# ロガーの設定
logging.basicConfig(level=logging.INFO)  # INFOレベル以上のログを記録
logger = logging.getLogger(__name__)

@app.post("/")
async def read_root(request: Request):
    # リクエストの受信をログに記録
    logger.info("Received a request")
    print('ログ出力テスト')
    try:
        # JSONデータの取得と解析
        data = await request.json()
        last_name = data.get("lastName")
        first_name = data.get("firstName")
        
        # デバッグ情報のログ記録
        logger.debug(f"Request Data: {data}")
        
        # 名前が存在する場合の処理
        if last_name and first_name:
            message = f"Hello, {last_name} {first_name}! from FastAPI"
            logger.info(f"Responding with message: {message}")
            return {"message": message}
        else:
            # 名前がない場合の処理
            logger.warning("No name provided in request")
            return {"message": "Hello, World! from FastAPI"}

    except Exception as e:
        # 例外発生時のエラーログ記録
        logger.error("An error occurred", exc_info=True)
        return {"message": "An error occurred during processing"}
