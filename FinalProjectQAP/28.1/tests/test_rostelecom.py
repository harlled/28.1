from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
import consts


def get_driver():

    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en-GB'})
    driver = webdriver.Chrome(executable_path=consts.driverPathChrome, chrome_options=options)

    driver.get(consts.baseUrl)
    driver.maximize_window()
    wait = WebDriverWait(driver, 40)
    assert wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="card-container__title"]'))).text == 'Авторизация'
    return driver, wait


def test_correct_redirect_to_register():
    driver, wait = get_driver()

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'
    driver.quit()

def test_registration_phoneNumber():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    wait.until(EC.presence_of_element_located((By.NAME, 'firstName'))).click()
    actionChain.send_keys('Аа').perform()
    wait.until(EC.presence_of_element_located((By.NAME, 'lastName'))).click()
    actionChain.send_keys('Вв').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address'))).click()
    actionChain.send_keys('9998887744').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))).click()
    actionChain.send_keys('Aabbccdd1').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password-confirm'))).click()
    actionChain.send_keys('Aabbccdd1').perform()
    driver.find_element(By.NAME, 'register').click()

    confirmPage = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Подтверждение телефона')]"))).text
    assert confirmPage == 'Подтверждение телефона'
    driver.quit()


def test_registration_email():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    wait.until(EC.presence_of_element_located((By.NAME, 'firstName'))).click()
    actionChain.send_keys('Аа').perform()
    wait.until(EC.presence_of_element_located((By.NAME, 'lastName'))).click()
    actionChain.send_keys('Вв').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address'))).click()
    actionChain.send_keys('test@tesdwat.ru').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))).click()
    actionChain.send_keys('Aabbccdd1').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password-confirm'))).click()
    actionChain.send_keys('Aabbccdd1').perform()
    driver.find_element(By.NAME, 'register').click()

    confirmPage = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Подтверждение email')]"))).text
    assert confirmPage == 'Подтверждение email'
    driver.quit()


def test_register_firstName_and_lastName():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    firstNameInput = wait.until(EC.presence_of_element_located((By.NAME, 'firstName')))
    lastNameInput = wait.until(EC.presence_of_element_located((By.NAME, 'lastName')))


    elementsDictionary = {
        'firstName': firstNameInput,
        'lastName': lastNameInput
    }

    for key in consts.registerKeysDict:
        values = consts.registerKeysDict[key]

        actionChain.click(elementsDictionary[key]).perform()

        for j in range(len(values)):
            actionChain.send_keys(values[j]).perform()
            driver.find_element(By.XPATH, "//p[contains(text(),'Личные данные')]").click()

            if j < len(values) - 1:
                if j >= 1:
                    pass
                else:
                    error = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'span.rt-input-container__meta.rt-input-container__meta--error'))).text
                assert error == consts.registerErrorsName
                actionChain.double_click(elementsDictionary[key]).click_and_hold().send_keys(Keys.DELETE).perform()
    driver.quit()


def test_register_email_and_phone():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    addressNameInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address')))

    values = consts.registerFormKeysAddress
    actionChain.click(addressNameInput).perform()

    for j in range(len(values)):
        actionChain.send_keys(values[j]).perform()
        driver.find_element(By.XPATH, "//p[contains(text(),'Личные данные')]").click()

        if j < len(values) - 1:
            if j >= 1:
                pass
            else:
                error = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'span.rt-input-container__meta.rt-input-container__meta--error'))).text
            assert error == consts.registerErrorsAddress
            time.sleep(1)
            actionChain.double_click(addressNameInput).click_and_hold().send_keys(Keys.DELETE).perform()
            time.sleep(1)
    driver.quit()


def test_register_password():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    passNameInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password')))

    values = consts.registerFormPassword
    actionChain.click(passNameInput).perform()

    for j in range(len(values)):
        actionChain.send_keys(values[j]).perform()
        driver.find_element(By.XPATH, "//p[contains(text(),'Личные данные')]").click()

        if j < len(values) - 1:
            if j >= 1:
                pass
            else:
                error = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'span.rt-input-container__meta.rt-input-container__meta--error'))).text

            time.sleep(1)
            actionChain.double_click(passNameInput).click_and_hold().send_keys(Keys.DELETE).perform()
            time.sleep(1)
            assert error == consts.regErPass
    driver.quit()


def test_register_passwordConfirm():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    wait.until(EC.presence_of_element_located((By.NAME, 'firstName'))).click()
    actionChain.send_keys('Аа').perform()
    wait.until(EC.presence_of_element_located((By.NAME, 'lastName'))).click()
    actionChain.send_keys('Вв').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address'))).click()
    actionChain.send_keys('9998887744').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))).click()
    actionChain.send_keys('Aabbccdd1').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password-confirm'))).click()
    actionChain.send_keys('Aabbccd1').perform()
    driver.find_element(By.NAME, 'register').click()

    error = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Пароли не совпадают')]"))).text
    assert error == 'Пароли не совпадают'
    driver.quit()


def test_click_forgotPassword():
    driver, wait = get_driver()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'
    driver.quit()


def test_refresh_captcha():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'

    oldCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')
    actionChain.move_to_element(driver.find_element(By.CLASS_NAME, 'rt-captcha__reload')).click().perform()

    driver.implicitly_wait(20)

    newCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')
    assert oldCaptcha != newCaptcha
    driver.quit()


def test_form_change():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'

    tabButtons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rt-tab')))
    assert wait.until(EC.title_is('Ростелеком ID'))
    assert len(tabButtons) == 4

    for i in range(len(tabButtons)):
        actionChain.move_to_element(tabButtons[i]).click().perform()
        placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
        assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-tab--active'))).text == driver.find_element(By.ID, consts.tabButtonsId[i]).text
        assert placeholderInput == consts.placeholderInputsValue[i]
    driver.quit()


def test_back_to_login():
    driver, wait = get_driver()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'

    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='reset-back']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Авторизация')]"))).text == 'Авторизация'
    driver.quit()


def test_correct_change_input():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    tabButtons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rt-tab')))
    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeValue[0]

    for i in range(len(tabButtons)):
        actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
        actionChain.send_keys(consts.sendedKeys[i]).perform()
        actionChain.move_to_element(driver.find_element(By.ID, 'password')).click().perform()
        activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
        assert activeTabButton.text == consts.tabTitlesAuth[i], driver.quit()

        time.sleep(1) # Имитация живого пользователя

        actionChain.double_click(driver.find_element(By.ID, 'username')).click_and_hold().send_keys(Keys.DELETE).perform()
        time.sleep(1)

    driver.quit()


def test_form_change_auth():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    tabButtons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rt-tab')))
    assert wait.until(EC.title_is('Ростелеком ID'))
    assert len(tabButtons) == 4

    for i in range(len(tabButtons)):
        actionChain.move_to_element(tabButtons[i]).click().perform()
        placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
        assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-tab--active'))).text == driver.find_element(By.ID, consts.tabButtonsId[i]).text
        assert placeholderInput == consts.placeholderInputsValue[i]


def test_try_auth_with_vk():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_vk'))).click()

    assert driver.current_url.__contains__('oauth.vk.com')
    driver.quit()


def test_try_auth_with_ok():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_ok'))).click()

    assert driver.current_url.__contains__('connect.ok.ru')
    driver.quit()


def test_try_auth_with_mail():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_mail'))).click()

    assert driver.current_url.__contains__('connect.mail.ru')
    driver.quit()


def test_try_auth_with_google():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_google'))).click()

    assert driver.current_url.__contains__('accounts.google.com')
    driver.quit()


def test_try_auth_with_yandex():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_ya'))).click()

    assert driver.current_url.__contains__('oauth.yandex.ru')
    driver.quit()


def test_tg_chat():
    driver, wait = get_driver()
    actionChains = ActionChains(driver)
    chatTg = wait.until(EC.presence_of_element_located((By.ID, "widget_bar")))
    originalWindow = driver.current_window_handle
    actionChains.move_to_element(chatTg).perform()
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="alt-channel omnichat-theme-white svelte-1sezl8s"][2]'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    assert driver.current_url.__contains__('https://telegram.me/Rostelecom_ChatBot')
    driver.quit()


def test_viber_chat():
    driver, wait = get_driver()
    actionChains = ActionChains(driver)
    chatVb = wait.until(EC.presence_of_element_located((By.ID, "widget_bar")))
    originalWindow = driver.current_window_handle
    actionChains.move_to_element(chatVb).perform()
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="alt-channel omnichat-theme-white svelte-1sezl8s"][1]'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    assert driver.current_url.__contains__('https://chats.viber.com/Rostelecom')
    driver.quit()


def test_open_agreement():
    driver, wait = get_driver()
    actionChains = ActionChains(driver)
    originalWindow = driver.current_window_handle

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'пользовательского соглашения'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    window_title = driver.execute_script("return window.document.title")
    assert window_title == 'User agreement'

    driver.close()

    driver.switch_to.window(originalWindow)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[1]'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    window_title = driver.execute_script("return window.document.title")
    assert window_title == 'User agreement'

    driver.close()

    driver.switch_to.window(originalWindow)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[2]'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    window_title = driver.execute_script("return window.document.title")
    assert window_title == 'User agreement'

    driver.quit()
