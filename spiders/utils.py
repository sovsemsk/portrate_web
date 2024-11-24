from selenium import webdriver


class Driver:
    def __init__(self):
        self._options = webdriver.ChromeOptions()
        self._options.set_capability("selenoid:options", {
            "enableVNC": True,
            "screenResolution": "1280x1024x24",
            "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru", "LC_ALL=ru_RU.UTF-8"]
        })
        self._driver = webdriver.Remote(command_executor="http://9bea7b5c.portrate.io/wd/hub", options=options)
        # self._driver = webdriver.Chrome()

    def __enter__(self):
        return self._driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.close()
        self._driver.quit()
