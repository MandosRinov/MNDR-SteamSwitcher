import winreg, keyboard, subprocess, json


def get_config():
    with open("config.json", "r") as f:
        return json.load(f)
    
def set_active_account(account):
    config = get_config()
    config["active_account"] = account
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

def switch_steam_account(username):
    active_account = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
    set_active_account(username)
    winreg.SetValueEx(active_account, "AutoLoginUser", 0, winreg.REG_SZ, username)
    winreg.CloseKey(active_account)

# def main(): 
#     keyboard.add_hotkey("ctrl+shift+l")
# switch_steam_account(get_steam_path())

set_active_account("mandanin1")
