def get_desired_caps(browser='chrome', device='R3CR403EKTE'):

    if browser == 'chrome':
        return {
            'platformName': 'Android',
            'browserName': 'Chrome',
            'automationName': 'uiautomator2',
            'deviceName': device
        }
    elif browser == 'firefox':
        return {
            'platformName': 'Windows',
            'appium:automationName': 'Gecko',
            'appium:deviceName': 'Samsung S9',
            'newCommandTimeout': 180,
            'browserName': 'MozillaFirefox',
            'moz:firefoxOptions': {
                'androidPackage': 'org.mozilla.firefox',
                'androidDeviceSerial': device
            }
        }

