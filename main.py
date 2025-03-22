import winreg, keyboard, subprocess, json
from time import sleep

def get_config():
    with open("config.json", "r") as f:
        return json.load(f)
    
def setKey(key, value):
    config = get_config()
    config[key] = value
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    
def getKey(key: str):
    config = get_config()
    return config[key]

def add_account(new_account):
    config = get_config()
    config["accounts"].append(str(new_account))
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def get_steam_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
        steam_path = winreg.QueryValueEx(key, "SteamExe")[0]
        winreg.CloseKey(key)
        return steam_path
    
    except Exception as e:
        print(f"Error getting Steam path: {e}")
        return None

def switch_steam_account(username: str):
    try:
        autoLoginUserRef = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
        active_account = winreg.QueryValueEx(autoLoginUserRef, "AutoLoginUser")[0]
        print("Change account from: ", active_account)

        winreg.SetValueEx(autoLoginUserRef, "AutoLoginUser", 0, winreg.REG_SZ, username)
        winreg.CloseKey(autoLoginUserRef)
        setKey("active_account",username)

        subprocess.Popen(["start", get_steam_path(), "-shutdown"], shell=True)
        sleep(2)
        subprocess.Popen(["start", "steam://open"], shell=True)
        
    except Exception as e:
        print(f"Error switching steam account: {e}")
        