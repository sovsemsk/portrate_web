from selenium import webdriver

def driver():
    options = webdriver.ChromeOptions()
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "screenResolution": "1280x1024x24",
        "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru", "LC_ALL=ru_RU.UTF-8"]
    })

    driver = webdriver.Remote(command_executor="http://9bea7b5c.portrate.io/wd/hub", options=options)
    return driver
