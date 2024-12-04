import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

CHROME_DRIVER_PATH = "chromedriver"
BASE_URL = "https://www.mse.mk/mk/stats/symbolhistory/"


def scrape_company_data(company_code):
    """Скрапира податоци за одредена компанија и ги зачувува во CSV."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Без GUI
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)

    try:
        # Отвори ја страницата
        url = f"{BASE_URL}{company_code}"
        driver.get(url)

        # Почекај да се појави табелата
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "resultsTable"))
        )

        # Собери ги редовите од табелата
        rows = []
        table = driver.find_element(By.CSS_SELECTOR, "#resultsTable tbody")
        for row in table.find_elements(By.TAG_NAME, "tr"):
            cells = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
            rows.append(cells)

        # Зачувај податоци во CSV
        if rows:
            df = pd.DataFrame(
                rows,
                columns=["Датум", "Цена на последна трансакција", "Макс.", "Мин.", "Просечна цена", "Количина",
                         "Промет во денари"]
            )
            df.to_csv(f"data/{company_code}.csv", index=False)
            print(f"Податоците за {company_code} се успешно зачувани.")

    except TimeoutException:
        print(f"Не можев да ги најдам податоците за {company_code}.")
    finally:
        driver.quit()


def get_existing_data(company_code):
    """Ги чита постоечките податоци за компанијата од CSV ако постојат."""
    file_path = f"data/{company_code}.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path).to_dict(orient='records')
    return None
