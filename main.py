from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Задание 1: Гистограмма для нормального распределения
mean = 0
std_dev = 1
num_samples = 1000
data = np.random.normal(mean, std_dev, num_samples)
plt.hist(data, bins=30, edgecolor='black')
plt.title('Гистограмма для нормального распределения')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.show()

# Задание 2: Диаграмма рассеяния
x = np.random.rand(100)
y = np.random.rand(100)
plt.scatter(x, y)
plt.title('Диаграмма рассеяния')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# Задание 3: Парсинг цен на диваны

# Запуск браузера
driver = webdriver.Chrome()

# Переход на страницу
url = 'https://www.divan.ru/category/divany-i-kresla'
driver.get(url)

# Поиск элементов на странице
divans = driver.find_elements(By.CLASS_NAME, '_Ud0k')

divan_data = []

for divan in divans:
    try:
        price = divan.find_element(By.CSS_SELECTOR, 'div.pY3d2 span').text.replace('руб.', '').replace(' ', '').strip()
    except Exception as e:
        print(f"Ошибка при обработке элемента: {e}")
        continue

    divan_data.append([price])

# Закрытие браузера
driver.quit()

# Сохранение данных в CSV файл
with open('divan_prices.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Цена'])
    writer.writerows(divan_data)

print("Данные успешно сохранены в файл divan_prices.csv")

# Загрузка данных из CSV файла
df = pd.read_csv('divan_prices.csv')

# Проверка первых строк данных
print(df.head())

# Преобразование столбца 'Цена' в числовой формат
df['Цена'] = pd.to_numeric(df['Цена'], errors='coerce')

# Удаление строк с отсутствующими или некорректными значениями
df.dropna(subset=['Цена'], inplace=True)

# Вычисление средней цены
average_price = df['Цена'].mean()
print(f'Средняя цена на диваны: {average_price:.2f} ₽')

# Построение гистограммы цен
plt.hist(df['Цена'], bins=30, edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (₽)')
plt.ylabel('Частота')
plt.show()
