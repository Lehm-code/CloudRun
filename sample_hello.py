# main.py

app = FastAPI()

# Cloud Loggingハンドラを標準loggingモジュールに接続する
log_client = google.cloud.logging.Client()
log_client.setup_logging()

# ロガーを取得
logger = logging.getLogger(__name__)

def search_with_selenium(query):
    # Chromeドライバの設定
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ヘッドレスモードでの実行
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # ドライバの起動
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # 検索ページを開く
    driver.get("https://www.google.com")
    
    try:
        # 検索ボックスを見つけて入力
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.submit()
        
        # ページが読み込まれるまで待機
        time.sleep(2)
        
        # 検索結果の取得（例として最初の5件を取得）
        results = driver.find_elements(By.CSS_SELECTOR, "h3")[:5]
        search_results = [result.text for result in results]
        
        logger.info(f"検索結果: {search_results}")
        return search_results
    except Exception as e:
        logger.error("Seleniumでの検索中にエラーが発生しました", exc_info=True)
        return ["検索結果の取得中にエラーが発生しました"]
    finally:
        driver.quit()

@app.post("/")
async def search_endpoint(request: Request):
    # リクエストの受信をログに記録
    logger.info("リクエストを受信しました")
    try:
        # JSONデータの取得と解析
        data = await request.json()
        query = data.get("query")
        
        # クエリが存在するかチェック
        if query:
            logger.debug(f"検索クエリ: {query}")
            
            # Seleniumを使って検索を実行
            results = search_with_selenium(query)
            return {"results": results}
        else:
            logger.warning("クエリが入力されていません。")
            return {"message": "検索クエリが必要です"}
    except Exception as e:
        # 例外発生時のエラーログ記録
        logger.error("エラー発生", exc_info=True)
        return {"message": "An error occurred during processing"}
