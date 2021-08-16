import os
from selenium import webdriver
from msedge.selenium_tools import EdgeOptions, Edge
import json
import functools


def webdriver(func):
    @functools.wraps(func)
    def driver_setup():
        browser, driverPath = func()
        if browser == "firefox":
            driver = webdriver.Firefox(
                executable_path=rf"{driverPath}",
            )
        elif browser == "edge":
            options = EdgeOptions()
            options.use_chromium = True
            driver = Edge(
                options=options,
                executable_path=rf"{driverPath}",
            )
        else:
            driver = webdriver.Chrome(
                executable_path=rf"{driverPath}",
            )
        driver.implicitly_wait(30)
        return driver
    return driver_setup()


@webdriver
def setup() -> tuple:
    settingfile = "popcat.json"

    if os.path.isfile(settingfile):
        with open(settingfile, "r") as readFile:
            data = json.load(readFile)
            return data.get("browser"), data.get("driverPath")
    browser = input("Please select a browser[edge, chrome, firefox]: ")
    driverPath = input("Enter the Driver path: ")
    data = {"browser": browser, "driverPath": driverPath}
    with open("popcat.json", "w") as outfile:
        json.dump(data, outfile, indent=2, sort_keys=True)
    return browser, driverPath


def main(driver):

    driver.get("https://popcat.click/")
    button = driver.find_element_by_xpath("/html/body/div[1]/img")
    try:
        while True:
            button.click()
    except KeyboardInterrupt:
        driver.quit()

if __name__ == "__main__":
    main(driver = setup)