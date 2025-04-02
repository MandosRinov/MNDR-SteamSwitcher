import winreg, keyboard, subprocess, json


def get_config() -> object:
    """
    return config with notes about current active user and various accounts
    """
    with open("config.json", "r") as f:
        return json.load(f)
    
def getKey(key: str):
    config = get_config()
    return config[key]

def setKey(key:str, value: str|object|list):
    config = get_config()
    config[key] = value
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

def get_steam_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam")
        steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
        winreg.CloseKey(key)
        return steam_path
    except Exception as e:
        print(f"Error getting Steam path: {e}")
        return None

def switch_steam_account(username: str):
    try:
        active_account = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
        setKey("active_account", username)
        winreg.SetValueEx(active_account, "AutoLoginUser", 0, winreg.REG_SZ, username)
        winreg.CloseKey(active_account)
    except Exception as e:
        print(f"Error with switching active user: {e}")



def main():
    current_active = getKey('active_account')
    
