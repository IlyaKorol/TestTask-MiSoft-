from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Настройки
EMAIL = "your_email"
PASSWORD = "your_password"
NEW_PASSWORD = "your_new_password"
BIRTHDAY = "your_birthday"
RESERVE_EMAIL = "your_reserve_email"

# Запуск браузера
driver = webdriver.Chrome()

try:
    wait = WebDriverWait(driver, 30)

    # Вход в аккаунт Gmail
    driver.get("https://mail.google.com/")

    # Ввод email
    email_input = wait.until(EC.visibility_of_element_located((By.ID, "identifierId")))
    email_input.send_keys(EMAIL)
    email_input.send_keys(Keys.RETURN)
    time.sleep(2)

    # Подождем, пока страница не загрузится и не появится поле ввода пароля
    password_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

    # Переход к безопасности аккаунта
    driver.get("https://myaccount.google.com/security")

    # Дополнительная диагностика - сделаем скриншот
    driver.save_screenshot('security_page.png')

    # Попробуем найти кнопку изменения пароля разными способами
    try:
        password_change_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='password']"))
        )
        print("Password change button found.")
        password_change_button.click()
    except Exception as e:
        print(f"Error finding password change button: {e}")
        driver.quit()
        exit(1)

    # Подождем, пока страница не загрузится
    time.sleep(5)

    # Введите новый пароль и подтвердите его
    try:
        # Используем более общий CSS-селектор для поиска всех полей ввода пароля
        password_fields = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        print(f"Number of password fields found: {len(password_fields)}")

        # Проверьте количество найденных полей и их порядковый номер
        if len(password_fields) == 2:
            new_password_input = password_fields[0]
            confirm_password_input = password_fields[1]

            print("Entering new password.")
            new_password_input.send_keys(NEW_PASSWORD)
            confirm_password_input.send_keys(NEW_PASSWORD)
            confirm_password_input.send_keys(Keys.RETURN)
        else:
            print("Error: Expected new password and confirm password input fields not found")
            driver.save_screenshot('error_screenshot_new_password.png')
            driver.quit()
            exit(1)
    except Exception as e:
        print(f"Error finding new password input: {e}")
        driver.save_screenshot('error_screenshot_new_password.png')
        driver.quit()
        exit(1)

    # Сохранение данных в таблицу
    data = {
        "Email": [EMAIL],
        "Password": [NEW_PASSWORD],
        "Birthday": [BIRTHDAY],
        "Reserve Email": [RESERVE_EMAIL],
    }

    df = pd.DataFrame(data)
    df.to_csv("gmail_account_info.csv", index=False)
    print("Report saved to gmail_account_info.csv")

finally:
    driver.quit()
