# Необходимые модули: selenium, requests
try:
    from selenium.common.exceptions import WebDriverException, InvalidSessionIdException, NoSuchWindowException
    from program import *
except BaseException as e:
    try:
        browser.quit()
    except Exception:
        pass
    if not isinstance(e, (InvalidSessionIdException, NoSuchWindowException, SystemExit, KeyboardInterrupt)):
        print("Исключение", type(e))
        print(e)
        input("Нажмите enter, чтобы закрыть это окно... ")
