"""
-----------------------------コードの注意・改善要素-------------------------------
・XPATHで絶対パスを使用している部分があるためサイトの変更に弱い
・判定時に一致していてもテストのため保留にしている
・判定時に1秒以内に描画が更新されないと前の条件で判定していしまう
・判定条件が動的に動作出来ていない
・エラー処理を追加していない
・ヘッドレストモードで行うかの確認等
・ユーザーエージェントに連絡先の明示
"""
# pipライブラリ
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
# .pyライブラリ
from lib.scraping import Scraper



class AirWork():
    header_css_dict = {
        'ホーム' : 'a.styles_menuLinkActive__EJpHO',
        '候補者' : 'a.styles_menuLink___TTEe',
        '応募者' : 'a.Mstyles_menuLink___TTEe',
        '求人' : 'a.styles_menuLink___TTEe',
        '有料広告' : 'a.styles_menuLink___TTEe',
        'その他' : 'a.styles_menuLink___TTEe',
    }

    css_element_dict = {
        '求人一覧' : 'table.styles_table__YW0pA',
    }

    # xpath_element_dict = {
    #     'チケット補充ポップアップ' : '/html/body/div[5]/div/div[6]/a',
    #     '1人目のプロフィール確認' : "//a[@data-modal_type='candidateModal' and @data-modal_param='.js_rowC1Param']",
    # }

    class_element_dict = {
        'ログインボタン' : 'primary'
    }


    # judge_action_dict = {
    #     'オファー': 'a.md_btn.md_btn--approach.js_modalCommit.js_candidateApproach',
    #     '拒否': 'a.md_btn.md_btn--dismiss.js_modalCommit.js_candidateDismiss',
    #     '保留': 'a.md_btn.md_btn--keep.js_modalCommit',
    # }

    def __init__(self, data):
        self.data = data

    def AirWorkScount(self):
        # カスタムユーザーエージェントを設定
        contact_url = "https://about.moricrew.com/" 
        user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 (Contact: {contact_url})"
        # オプションの設定
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f"user-agent={user_agent}")
        # ブラウザを起動
        driver = webdriver.Chrome(options=chrome_options)
        # 初期画面のサイトにアクセス
        url = "https://ats.rct.airwork.net/interaction"
        driver.get(url)
        # ログインをクリック
        class_name = "styles_loginButton__XULr9"
        Scraper.ClickElement_CLASS(driver, class_name)
        # ログイン情報の入力とログイン
        id_name = 'account'
        input_text = self.data['login_id']
        Scraper.InputElement_ID(driver, id_name, input_text)
        id_name = 'password'
        input_text = self.data['login_pass']
        Scraper.InputElement_ID(driver, id_name, input_text)
        class_name = self.class_element_dict['ログインボタン']
        Scraper.ClickElement_CLASS(driver, class_name)
        # ヘッダーから選択
        css_selector_name = self.header_css_dict['候補者']
        Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
        # テーブルデータを取得して候補者選択
        table_data = self.Get_Job_Table(driver)
        css_selector_name = f"a[data-la='candidates_search_link_click'][data-la-job-id='{table_data[0][0]}']"
        Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
        # 求人者情報の取得
        page = 0
        self.Get_Detail_Table(driver, page)
        # 次のページへ移行
        css_selector_name = 'a.styles_paginateItemLink__7yRM6.styles_next__3LCdl'
        Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
        # 求人者情報の取得
        page = 1
        self.Get_Detail_Table(driver, page)

        driver.quit()
        message = {"result" : "OK"}
        return message


    def AirworkUpdate(self, data):
        # カスタムユーザーエージェントを設定
        contact_url = "https://about.moricrew.com/" 
        user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 (Contact: {contact_url})"
        # オプションの設定
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f"user-agent={user_agent}")
        # ブラウザを起動
        driver = webdriver.Chrome(options=chrome_options)
        # 初期画面のサイトにアクセス
        url = "https://ats.rct.airwork.net/interaction"
        driver.get(url)
        # ログインをクリック
        class_name = "styles_loginButton__XULr9"
        Scraper.ClickElement_CLASS(driver, class_name)
        # ログイン情報の入力とログイン
        id_name = 'account'
        input_text = self.data['login_id']
        Scraper.InputElement_ID(driver, id_name, input_text)
        id_name = 'password'
        input_text = self.data['login_pass']
        Scraper.InputElement_ID(driver, id_name, input_text)
        class_name = self.class_element_dict['ログインボタン']
        Scraper.ClickElement_CLASS(driver, class_name)
        # ヘッダーから選択
        css_selector_name = self.header_css_dict['求人']
        Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
        # 求人一覧の選択
        css_selector_name = self.css_element_dict['求人一覧']
        message = self.GetTableAsData_AirworkUpdate(driver, css_selector_name)
        driver.quit()
        return message









    ################################################################################

    def Get_Job_Table(self, driver):
        '''
        テーブル内の全行とセルの情報を取得し、リスト形式で保存
        '''
        target_url = "https://ats.rct.airwork.net/candidates"
        WebDriverWait(driver, 5).until(lambda driver: driver.current_url == target_url)
        table_data = []
        # テーブルの取得
        table = driver.find_element(By.CSS_SELECTOR, "table.styles_table__YW0pA")  # CSSセレクタでテーブルを特定
        rows = table.find_elements(By.TAG_NAME, "tr")  # 行（<tr>）要素を取得
        # 各行のデータを取得
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")  # セル（<td>）要素を取得
            row_data = [cell.text for cell in cells]  # 各セルのテキストをリストに追加
            if row_data:  # 空行は無視
                table_data.append(row_data)
        for i in range(len(table_data)):
            table_data[i] = table_data[i][0:2]
        # 結果の表示
        print(table_data)
        return table_data

    def Get_Detail_Table(self, driver, page):
        print(f'{page + 1}ページ目です。')
        details = []
        try:
            # data-jobseeker-cassetteの要素をすべて取得
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-jobseeker-cassette]"))
            )
        # 各要素からcassette_id、年齢、都道府県を取得
            for candidate in element:
                # cassette_idの取得
                cassette_id = candidate.get_attribute("data-jobseeker-cassette")
                # 年齢の取得（最初の<p>タグ）
                age = candidate.find_elements(By.CSS_SELECTOR, "p")[0].text
                # 都道府県の取得（3番目の<p>タグ）
                prefecture = candidate.find_elements(By.CSS_SELECTOR, "p")[2].text
                # 必要な情報をリストとして追加
                details.append([f"{page*50+int(cassette_id) + 1}人目", age, prefecture])

        except Exception as e:
            print("情報の取得に失敗しました:", e)
        print(details)

    def GetTableAsData_AirworkUpdate(self, driver, css_selector_name):
        '''
        HTMLのテーブル要素をCSSセレクタから取得し、pandasのDataFrameとして返します。
        '''
        try:
            # CSSセレクタに基づくテーブル要素の取得
            table_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_name))
            )            
            # data-work_id属性を持つ<tr>要素のみを取得
            rows = table_element.find_elements(By.XPATH, "tr")
            # テーブルデータを格納するリスト
            table_data = []
            # 各行のデータを抽出
            for row in rows:
                # data-work_idの値を取得
                work_id = row.get_attribute("data-work_id")
                # タイトル（<a>タグのテキスト）の取得
                column_1_element = row.find_element(By.XPATH, ".//td[1]/div[1]/a")
                column_1_text = column_1_element.text
                # 選択されている<option>のテキストを取得
                try:
                    column_2_element = row.find_element(By.XPATH, ".//td[6]/span/select/option[@selected]")
                    column_2_text = column_2_element.text
                except Exception as e:
                    column_2_text = "取得失敗"  # オプションが見つからない場合のデフォルト値
                # 条件に基づいて行データを追加
                if column_2_text == "公開中":
                    row_data = [work_id, column_1_text] 
                    table_data.append(row_data)
            # DataFrameに変換（最初の列をwork_idとし、他の列名を適宜設定）
            df = pd.DataFrame(table_data, columns=["joc_code", "job_title"])
            json_data = df.to_json(orient="records", force_ascii=False)
            message = {
                "求人": json_data,
                "result": "完了しました"
            }
            print(message)
            return message
        except Exception as e:
            print(f"{css_selector_name}要素が見つかりません。エラー内容: {e}")
            message = {"result" : "公開中の一覧を取得できませんでした。"}
            return message


################################################################################

if __name__ == "__main__":
    pass

