import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('./chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')
   yield
   pytest.driver.quit()

def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('sergo123@mail.ru')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('123321')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Нажимаем на кнопку бургера
   pytest.driver.find_element_by_xpath('//span[@class="navbar-toggler-icon"]').click()
   # Нажимаем на кнопку "Мои питомцы"
   pytest.driver.find_element_by_xpath('//a[@class="nav-link" and @href="/my_pets"]').click()
   # Сохраняем в переменную элементы статистики
   pets_statistic = pytest.driver.find_elements_by_xpath('//div[@class=".col-sm-4 left"]')
   # Получаем количество питомцев из данных статистики
   number = pets_statistic[0].text.split('\n')
   number = number[1].split(' ')
   number = int(number[1])
   # Находим количество питомцев на странице
   pets = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr")))
   #pets = pytest.driver.find_elements_by_xpath('//tbody/tr')
   # Сохраняем в переменную количество питомцев с фото и без фото
   pytest.driver.implicitly_wait(5)
   with_photo = pytest.driver.find_elements_by_xpath('//img[contains(@src, "jpeg")]')
   without_photo = pytest.driver.find_elements_by_xpath('//img[@src=""]')
   # Сохраняем имена питомцев в переменную
   names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
   # Сохраняем породу питомцев в переменную
   breed = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')
   # Сохраняем возраст питомцев в переменную
   age = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')

   for i in range (len(pets)):
      # Сравниваем количество питомцев на странице и количество питомцев из статистики
      assert len(pets) == number
      # Сравниваем количество питомцев с фото и без фото
      assert len(with_photo) > len(without_photo)
      # Сравниваем количество имён, пород и возрастов в массивах с количеством питомцев из статистики
      assert len(names) == number
      assert len(breed) == number
      assert len(age) == number
      # Проверяем уникальность имен питомцев
      assert names[0].text != names[1].text
      assert names[0].text != names[2].text
      assert names[0].text != names[3].text
      assert names[1].text != names[2].text
      assert names[1].text != names[3].text
      assert names[2].text != names[3].text
      # Проверяем питомцев на уникальность
      assert names[0].text != names[1].text and breed[0].text != breed[1].text and age[0].text != age[1].text
      assert names[0].text != names[2].text and breed[0].text != breed[2].text and age[0].text != age[2].text
      assert names[0].text != names[3].text and breed[0].text != breed[3].text and age[0].text != age[3].text
      assert names[1].text != names[2].text and breed[1].text != breed[2].text and age[1].text != age[2].text
      assert names[1].text != names[3].text and breed[1].text != breed[3].text and age[1].text != age[3].text
      assert names[2].text != names[3].text and breed[2].text != breed[3].text and age[2].text != age[3].text