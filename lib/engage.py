"""
-----------------------------コードの注意・改善要素-------------------------------
・判定時に一致していてもテストのため保留にしている
・判定時に1秒以内に描画が更新されないと前の条件で判定していしまう
・判定条件が動的に動作出来ていない
・エラー処理を追加していない
"""
# pipライブラリ
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
# .pyライブラリ
from lib.scraping import Scraper




class Engage():
    header_css_dict = {
        '候補者管理' : 'a.MuiTypography-root.MuiTypography-body1Strong.MuiLink-root.MuiLink-underlineNone.mui-1z6cjm',
        '採用ページ' : 'a.MuiTypography-root.MuiTypography-body1Strong.MuiLink-root.MuiLink-underlineNone.mui-gh8y1z',
        '求人作成・管理' : 'a.MuiTypography-root.MuiTypography-body1Strong.MuiLink-root.MuiLink-underlineNone.mui-zmyvy7',
        'DM' : 'a.MuiTypography-root.MuiTypography-body1Strong.MuiLink-root.MuiLink-underlineNone.mui-gh8y1z',
    }

    css_element_dict = {
        'チケットポップアップ' : 'button.MuiButtonBase-root.MuiButton-textPrimary',
        '求人一覧' : '.md_table.md_table--sortable'
    }

    xpath_element_dict = {
        'チケット補充ポップアップ' : '/html/body/div[5]/div/div[6]/a',
        '1人目のプロフィール確認' : "//a[@data-modal_type='candidateModal' and @data-modal_param='.js_rowC1Param']",
    }

    id_element_dict = {
        'ログインボタン' : 'login-button'
    }

    judge_action_dict = {
        'オファー': 'a.md_btn.md_btn--approach.js_modalCommit.js_candidateApproach',
        '拒否': 'a.md_btn.md_btn--dismiss.js_modalCommit.js_candidateDismiss',
        '保留': 'a.md_btn.md_btn--keep.js_modalCommit',
    }

    def __init__(self, data):
        self.data = data

################################################################################

    def EngageScount(self):
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
        url = "https://en-gage.net/company_login/login/"
        driver.get(url)
        # ログイン情報の入力とログイン
        id_name = 'loginID'
        input_text = self.data['login_id']
        Scraper.InputElement_ID(driver, id_name, input_text)
        id_name = 'password'
        input_text = self.data['login_pass']
        Scraper.InputElement_ID(driver, id_name, input_text)
        id_name = self.id_element_dict['ログインボタン']
        Scraper.ClickElement_ID(driver, id_name)
        # 「チケットが残り少ないです」のポップアップを消す
        css_selector_name = self.css_element_dict['チケットポップアップ']
        Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
        # ヘッダーの選択
        css_selector_name = self.header_css_dict['候補者管理']
        Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
        # 「オススメの新着スカウト候補者がいますケットが残り少ないです」のポップアップを消す
        xpath_name = self.xpath_element_dict['チケット補充ポップアップ']
        Scraper.ClickElement_XPATH(driver, xpath_name)
        # 1人目のプロフィール確認に対してクリックする
        xpath_name = self.xpath_element_dict['1人目のプロフィール確認']
        Scraper.ClickElement_XPATH(driver, xpath_name)
        # プロフィールデータを取得
        print('判定条件は以下の項目です。')
        print(self.data)
        for i in range(self.data['judge_count']):
            profile_data = self.Get_Profile_Data(driver)
            print(f"{i+1}人目")
            print(profile_data)
            # 判定の結果を格納する辞書を用意
            judge_results = {}
            # 判定処理
            # 性別
            judge_results['gender'] = profile_data['性別'] == self.data['gender']
            # 年齢
            judge_results['age'] = profile_data['年齢'].replace('歳', '') in [str(age).replace('歳', '') for age in self.data['age']]
            # 現住所（部分一致）
            judge_results['address'] = self.data['address'] in profile_data['現住所']
            # 全ての判定結果がTrueの場合にテキストを表示
            if all(judge_results.values()):
                print("全ての条件に一致したのでオファーします。")
                # テストではオファーしないため「保留」の方を押している
                css_selector_name = self.judge_action_dict['保留']
                Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
            else:
                print("条件に一致しない項目があるので拒否します。")
                css_selector_name = self.judge_action_dict['拒否']
                Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
            # 描画待ち&連続アクセスのインターバル(必須)
            time.sleep(1)


        driver.quit()
        message = {"result" : "OK"}
        return message


    def EngageUpdate(self):
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
        url = "https://en-gage.net/company_login/login/"
        driver.get(url)
        # ログイン情報の入力とログイン
        id_name = 'loginID'
        input_text = self.data['login_id']
        Scraper.InputElement_ID(driver, id_name, input_text)
        id_name = 'password'
        input_text = self.data['login_pass']
        Scraper.InputElement_ID(driver, id_name, input_text)
        id_name = self.id_element_dict['ログインボタン']
        Scraper.ClickElement_ID(driver, id_name)
        # 「チケットが残り少ないです」のポップアップを消す
        css_selector_name = self.css_element_dict['チケットポップアップ']
        Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
        # ヘッダーの選択
        css_selector_name = self.header_css_dict['求人作成・管理']
        Scraper.ClickElement_CSS_SELECTOR(driver, css_selector_name)
        # ヘッダーの選択
        css_selector_name = self.css_element_dict['求人一覧']
        message = self.GetTableAsData_EngageUpdate(driver, css_selector_name)
        driver.quit()
        return message


################################################################################

    def Get_Profile_Data(self, driver):
        '''
        <dt>項目名と<dd>そのデータを順に取得し、辞書に保存
        '''
        profile_data = {}
        try:
            # 全ての<dt>と<dd>を取得
            dt_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".md_horizonTable .item"))
            )
            dd_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".md_horizonTable .data"))
            )
            
            # 辞書に<dt>と<dd>のテキストを保存
            for dt, dd in zip(dt_elements, dd_elements):
                profile_data[dt.text] = dd.text
        
        except Exception as e:
            print(f"データの取得に失敗しました。エラー: {e}")
        
        return profile_data

    def GetTableAsData_EngageUpdate(self, driver, css_selector_name):
        '''
        HTMLのテーブル要素をCSSセレクタから取得し、pandasのDataFrameとして返します。
        '''
        try:
            # CSSセレクタに基づくテーブル要素の取得
            table_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_name))
            )            
            # data-work_id属性を持つ<tr>要素のみを取得
            rows = table_element.find_elements(By.XPATH, ".//tr[@data-work_id]")
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



if __name__ == "__main__":
    pass