import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

import multiprocessing as mp
from multiprocessing import Manager


CONTEST_CODE = "START160A"
PROCESS_LIMIT=6

# create a new Chrome session
driver = webdriver.Chrome()
# make the browser full screen
driver.maximize_window()

def checkStanding(handle, data):
    print(f"Opening {handle}")
    driver.get(f"https://www.codechef.com/rankings/{CONTEST_CODE}?itemsPerPage=100&order=asc&page=1&search={handle}")
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "_scored-problems__header_t8ea1_196")))
    try:
        row = driver.find_element(By.ID, "MUIDataTableBodyRow-0")
    except:
        print("Not found!")
        return
    elements = row.find_elements(By.XPATH, ".//td/div[2]/*")
    elements_list = [element.text for element in elements]
    elements_list[1] = handle
    data[handle] = elements_list


def main():
    manager = Manager()
    data = manager.dict()
    pool = mp.Pool(PROCESS_LIMIT)

    jobs = []        

    with open('handles.txt') as f:
        handles = f.read().splitlines()

    for handle in handles:
        jobs.append(pool.apply_async(checkStanding, (handle, data,)))

    for job in jobs:
        job.get()

    pool.close()
    pool.join()

    print(data)

    values = list(data.values())
    values.sort(key=lambda x: int(x[0]))
    # close the browser window
    driver.quit()

    with open(f"{CONTEST_CODE}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(values)


if __name__ == '__main__':
    main()

