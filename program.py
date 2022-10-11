import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from random import random

options = ChromeOptions()
options.add_argument("--start-maximized")

# selenium бросит исключение, если установнена не последняя версия chromedriver
try:
    browser = webdriver.Chrome(options=options)
except (SessionNotCreatedException, WebDriverException):
    import requests
    import zipfile

    print("Установка последней версии chromedriver...")
    version = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
    file = requests.get(f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip",
                        allow_redirects=True)
    with open("chromedriver_bin.zip", 'wb') as chrome_driver_file:
        chrome_driver_file.write(file.content)
    archive = zipfile.ZipFile('chromedriver_bin.zip')
    archive.extract('chromedriver.exe')
    archive.close()
    browser = webdriver.Chrome(options=options)

# Загрузка логина и пароля
with open('settings.json') as file:
    settings = json.load(file)

browser.get('https://www.cambridgelms.org/think')
if settings["automatic_password_entry"]:
    login_xpath = '//*[@id="gigya-loginID-33136461830823732"]'
    password_xpath = '//*[@id="gigya-password-272446220556026"]'
    log_in_button_xpath = '//*[@id="gigya-login-form"]/div[2]/div[1]/div[4]/input'

    # Ввод логина и пароля
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, login_xpath)))
    time.sleep(settings["wait_for_the_password_field_load"])
    browser.find_element(By.XPATH, login_xpath).send_keys(settings["login"])
    browser.find_element(By.XPATH, password_xpath).send_keys(settings["password"])
    browser.find_element(By.XPATH, log_in_button_xpath).click()

    WebDriverWait(browser, 10).until(lambda d: browser.current_url in [
        'https://www.cambridgelms.org/main/p/en/session/limit',
        'https://www.cambridgelms.org/main/p/en/frontpage'
    ])

    time.sleep(0.05)

    # Предупреждение о многократной авторизации
    if browser.current_url == 'https://www.cambridgelms.org/main/p/en/session/limit':
        browser.find_element(By.XPATH, '//*[@id="session-limit-page"]/div/a[2]').click()
        WebDriverWait(browser, 10).until(
            lambda d: browser.current_url == 'https://www.cambridgelms.org/main/p/en/frontpage')
        time.sleep(0.05)


def type1():
    # Place boxes on the right places
    elements = browser.find_elements(By.XPATH, '//div[@class="arrastrableConFondo_KidsBox arrastrarComponent real '
                                               'activo" and @correcto]')
    used = set()
    if elements:
        match = []
        for el in elements:
            other_id = next(filter(lambda x: x not in used, el.get_attribute("correcto").split(',')))
            used.add(other_id)
            try:
                match.append((
                    el,
                    browser.find_element(By.XPATH, f'//div[@id="divDestinoArrastrar_{other_id}"]'),
                ))
            except Exception as e:
                print(other_id)
                raise e
        for a, b in match:
            try:
                a.click()
                b.click()
                time.sleep(0.3)
            except Exception as e:
                print(e)
    return len(elements) != 0


def type2():
    # True/false choose
    elements = browser.find_elements(By.XPATH, '//div[@class="verdaderoFalso_KidsBox verdaderoFalsoComponent '
                                               'real" and @correcto]')
    if elements:
        answers = []
        for el in elements:
            answer = el.get_attribute("correcto")
            try:
                answers.append(el.find_element(By.XPATH, f'div[@correcto="{answer}"]'))
            except Exception as e:
                print(answer)
                raise e
        for el in answers:
            try:
                el.click()
                time.sleep(0.02)
            except Exception as e:
                print(e)
    return len(elements) != 0


def type3():
    # Text fields
    elements = browser.find_elements(By.XPATH,
                                     '//input[@class="textoEditableConFondo_KidsBox textoEditableComponent '
                                     'real" and @soltext]')
    if elements:
        answers = []
        for el in elements:
            try:
                answer = el.get_attribute("soltext").split('|')[0]
                answers.append((el, answer))
            except Exception as e:
                print(e)
        for el, ans in answers:
            try:
                el.send_keys(ans)
                time.sleep(0.02)
            except Exception as e:
                print(e)
    return len(elements) != 0


def type4():
    # Select
    elements = browser.find_elements(By.XPATH, '//select[@class="combo_KidsBox comboComponent" and @correcto]')
    if elements:
        answers = []
        for el in elements:
            try:
                ans_i = int(el.get_attribute("correcto")) + 1
                answers.append((el, ans_i))
            except Exception as e:
                print(e)
        for el, ans_i in answers:
            try:
                select = Select(el)
                select.select_by_index(ans_i)
                time.sleep(0.02)
            except Exception as e:
                print(e)
    return len(elements) != 0


def type5():
    # Match with lines
    elements = browser.find_elements(By.XPATH, '//div[@class="divInitPointFlechas real" and @correcto]')
    used = set()
    if elements:
        match = []
        for el in elements:
            other_id = next(filter(lambda x: x not in used, el.get_attribute("correcto").split(',')))
            used.add(other_id)
            try:
                match.append((
                    el,
                    browser.find_element(By.XPATH, f'//div[@id="{other_id}"]'),
                ))
            except Exception as e:
                print(other_id)
                raise e
        for a, b in match:
            try:
                a.click()
                b.click()
                time.sleep(0.1)
            except Exception as e:
                print(e)
    return len(elements) != 0


def type6():
    # Crossword
    elements = browser.find_elements(By.XPATH, '//input[@data-letra]')
    if elements:
        answers = []
        for el in elements:
            try:
                answer = el.get_attribute("data-letra")
                answers.append((el, answer))
            except Exception as e:
                print(e)
        for el, ans in answers:
            try:
                el.send_keys(ans)
                time.sleep(0.01)
            except Exception as e:
                print(e)
    return len(elements) != 0


def type7():
    # Put in the right order
    elements = browser.find_elements(By.XPATH, '//div[@class="rdSeleccionOrdenar_KidsBox '
                                               'simboloRBSeleccionOrdenarComponent" and @correcto]')
    if elements:
        elements.sort(key=lambda el: int(el.get_attribute("correcto")))
        for el in elements:
            try:
                el.click()
                time.sleep(0.1)
            except Exception as e:
                print(e)
    return len(elements) != 0


def type8():
    # Choose a circle with a true statement
    elements = browser.find_elements(By.XPATH, '//div[@class="rdSeleccionUnica_rb_KidsBox '
                                               'simboloRBSeleccionUnicaComponent" and @correcto]')
    if elements:
        for el in elements:
            correct = el.get_attribute('correcto')
            if correct == 'false':
                continue
            elif correct != 'true':
                return False
            try:
                el.click()
                time.sleep(0.1)
            except Exception as e:
                print(e)
    return len(elements) != 0



def switch_to_scorm_content():
    browser.switch_to.default_content()
    browser.switch_to.frame("content-iframe")
    browser.switch_to.frame("ScormContent")


def next_button_click():
    while True:
        try:
            browser.switch_to.default_content()
            browser.find_element(By.XPATH, '//a[@class="item-link enabled f-right"]').click()
            break
        except Exception:
            print("Не могу найти кнопку `check`")


delay_coeff1 = settings["max_delay_between_tasks"] - settings["min_delay_between_tasks"]
delay_coeff2 = settings["min_delay_between_tasks"]
input("Нажмите `enter`, чтобы начать")
start_time = datetime.utcnow()
while True:

    _ = browser.window_handles  # Check if browser is closed
    if (datetime.utcnow() - start_time).total_seconds() > settings["next_task_page_loading_time_limit"]:
        print("Не могу решить эту задачу, перехожу к следующей...")
        next_button_click()
        time.sleep(5)
        start_time = datetime.utcnow()
    try:
        switch_to_scorm_content()
        time.sleep(0.2)
    except Exception:
        continue

    if not (type1() or type2() or type3() or type4() or type5() or type6() or type7() or type8()):
        continue

    t = random() * delay_coeff1 + delay_coeff2
    print(f"Жду {t} секунд перед отправкой задания...")
    time.sleep(t)
    while True:
        try:
            switch_to_scorm_content()
            browser.find_element(By.XPATH, '//div[@intentos="2"]').click()
            break
        except Exception:
            print("Не могу найти кнопку `check`")
    time.sleep(1)
    next_button_click()
    time.sleep(1)
    start_time = datetime.utcnow()
