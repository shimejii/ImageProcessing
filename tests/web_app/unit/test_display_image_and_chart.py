# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pathlib import Path

# URL = 'http://127.0.0.1:5000'
# POINT1 = '/'
# POINT2 = '/process'

# @pytest.fixture
# def browser():
#     # テストごとに新しいブラウザインスタンスを生成
#     driver = webdriver.Chrome()
#     yield driver
#     # テストが終了したらブラウザを閉じる
#     driver.quit()

# def test_html_rendering(browser):
#     # POST /
#     ## file upload by gui
#     browser.get(URL)
#     file_input = browser.find_element(By.NAME, "file")
#     file_path = Path('./s_bmp/win-32.bmp').resolve()
#     file_input.send_keys(str(file_path))
#     upload_button = browser.find_element(By.CLASS_NAME, "btn-primary")
#     upload_button.click()

#     # GET /process
#     ## get process ui
#     WebDriverWait(browser, 10).until(EC.url_changes(URL))
#     WebDriverWait(browser, 10).until(EC.title_contains("process windows bitmap file"))

#     # 例: イメージが表示されていることを確認
#     image_element = browser.find_element(By.TAG_NAME,'img')
#     assert image_element.is_displayed()

#     nav_tab = browser.find_element(By.XPATH, '/html/body/ul/li[2]/a')
#     nav_tab.click()

#     # 例: ヒストグラムが表示されていることを確認
#     histgram_canvas_red = browser.find_element(By.ID,'histgram_canvas_red')
#     assert histgram_canvas_red.is_displayed()
#     histgram_canvas_green = browser.find_element(By.ID, 'histgram_canvas_green')
#     assert histgram_canvas_green.is_displayed()
#     histgram_canvas_blue = browser.find_element(By.ID, 'histgram_canvas_blue')
#     assert histgram_canvas_blue.is_displayed()