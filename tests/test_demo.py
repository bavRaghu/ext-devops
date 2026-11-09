import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
            )
    )
    driver.maximize_window()
    yield driver
    driver.quit()


def get_alert_text(driver):
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    text = alert.text
    alert.accept()
    return text


def test_empty_name(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")
    driver.find_element(By.ID, "n").clear()
    driver.find_element(By.ID, "pw").send_keys("password")
    driver.find_element(By.ID, "sub").click()
    alert_text = get_alert_text(driver)
    assert alert_text == "Name should not be empty", "TEST FAILED. EMPTY USERNAME."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.ID, "n").send_keys("username")
    driver.find_element(By.ID, "pw").clear()
    driver.find_element(By.ID, "sub").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password should not be empty", "TEST FAILED. EMPTY PASSWORD."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.ID, "n").send_keys("username")
    driver.find_element(By.ID, "pw").send_keys("p")
    driver.find_element(By.ID, "sub").click()

    alert_text = get_alert_text(driver)
    assert alert_text == "Password should be at least 6 characters", "TEST FAILED. SHORT PASSWORD."


def test_valid_registration(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")
    driver.find_element(By.ID, "n").send_keys("username")
    driver.find_element(By.ID, "pw").send_keys("password")
    driver.find_element(By.ID, "sub").click()
    WebDriverWait(driver, 5).until(
        EC.url_contains("/register")
    )
    curr_url = driver.current_url
    assert "/register" in curr_url, "TEST FAILED. NOT ROUTED TO SUCCESS PAGE."
    body = driver.find_element(By.TAG_NAME, "body").text
    assert "Registration Successful" in body, "TEST FAILED. APPROPRIATE MESSAGE NOT DISPLAYED."
