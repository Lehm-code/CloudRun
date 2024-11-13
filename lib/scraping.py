from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def GetElement_CSS_SELECTOR(driver, css_selector_name):
        '''
        HTMLのエレメントに対してCSS_SELECTOR名を元にテキストを取得します。
        '''
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector_name))
            )
            text_content = element.text
            print(f"{css_selector_name}から「{text_content}」を取得しました。")
        except Exception as e:
            print(f"{css_selector_name}のテキストが取得出来ませんでした。")

    def GetElement_XPATH(driver, xpath_name):
        '''
        HTMLのエレメントに対してXPATH名を元にテキストを取得します。
        '''
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath_name))
            )
            text_content = element.text
            print(f"{xpath_name}から「{text_content}」を取得しました。")
        except Exception as e:
            print(f"{xpath_name}のテキストが取得出来ませんでした。")


################################################################################

    def ClickElement_CSS_SELECTOR(driver, css_selector_name):
        '''
        HTMLのエレメントに対してCSS_SELECTOR名を元にクリックします。
        '''
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector_name))
            )
            button.click()
            print(f"{css_selector_name}をクリックしました。")
        except Exception as e:
            print(f"{css_selector_name}要素が見つかりません。")

    def ClickElement_CLASS(driver, class_name):
        '''
        HTMLのエレメントに対してCLASS名を元にクリックします。
        '''
        try:
            element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, class_name))
            )
            element.click()
            print(f"{class_name}をクリックしました。")
        except Exception as e:
            print(f"{class_name}要素が見つかりません。")

    def ClickElement_ID(driver, id_name):
        '''
        HTMLのエレメントに対してID名を元にクリックします。
        '''
        try:
            element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, id_name))
            )
            element.click()
            print(f"{id_name}をクリックしました。")
        except Exception as e:
            print(f"{id_name}要素が見つかりません。")

    def ClickElement_XPATH(driver, xpath_name):
        '''
        HTMLのエレメントに対してXPATH名を元にクリックします。
        '''
        try:
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath_name))
            )
            button.click()
            print(f"{xpath_name}をクリックしました。")
        except Exception as e:
            print(f"{xpath_name}要素が見つかりません。")

################################################################################

    def InputElement_ID(driver, id_name, input_text):
        '''
        HTMLのエレメントに対してID名を元にテキストを入力します。
        '''
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, id_name))
            )
            element.send_keys(input_text) 
            print(f"{id_name}が入力されました。")
        except Exception as e:
            print(f"{id_name}要素が見つかりません。")





if __name__ == "__main__":
    pass