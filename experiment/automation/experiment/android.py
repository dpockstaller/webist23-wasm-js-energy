import subprocess, re


def install_apk(apk):
    subprocess.check_output("adb install -r -d -g " + apk, shell=True)


def kill_all():
    # kill all background processes
    subprocess.check_output("adb shell am kill-all", shell=True)


def open_chrome(url=""):
    if url:
        url = '-d {}'.format(url)

    subprocess.check_output('adb shell am start -n com.android.chrome/com.google.android.apps.chrome.Main {}'.format(url), shell=True)


def open_firefox(url=""):
    if url:
        url = '-d {}'.format(url)

    subprocess.check_output('adb shell am start -a android.intent.action.VIEW -n org.mozilla.firefox/org.mozilla.gecko.BrowserApp {}'.format(url), shell=True)


def tap(x, y):
    subprocess.check_output('adb shell input tap {} {}'.format(x, y), shell=True)


def clear_firefox():
    subprocess.check_output('adb shell pm clear org.mozilla.firefox', shell=True)


def clear_chrome():
    # https://stackoverflow.com/questions/60444428/android-skip-chrome-welcome-screen-using-adb
    subprocess.check_output('adb shell pm clear com.android.chrome', shell=True)
    subprocess.check_output('adb shell am set-debug-app --persistent com.android.chrome', shell=True)


def open_browser(browser, url):
    if browser == 'firefox':
        open_firefox(url)
    else:
        open_chrome(url)


def clear_browser(browser):
    if browser == 'firefox':
        clear_firefox()
    else:
        clear_chrome()


def unlock():
    subprocess.check_output('adb shell input keyevent 82',  shell=True)


def wakeup():
    subprocess.check_output('adb shell input keyevent 26',  shell=True)


def screen_brightness(brightness):
    brightness = int((brightness if brightness >= 0 and brightness <= 1 else .5) * 255)
    subprocess.check_output('adb shell settings put system screen_brightness {}'.format(brightness), shell=True)


def get_ip():
    net_output = subprocess.check_output(
        "adb shell ip -f inet addr show wlan0",
        shell=True,
        universal_newlines=True
    )
    return re.search(r"inet \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", net_output).group()[5:]


def connect_wifi(ip_address):
    subprocess.check_output('adb tcpip 5555', shell=True)
    subprocess.check_output('adb connect {}'.format(ip_address), shell=True)


def get_device_model():
    return subprocess.check_output("adb shell getprop ro.product.model", shell=True, universal_newlines=True).strip()
