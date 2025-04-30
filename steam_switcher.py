import winreg, psutil as ps
from time import sleep

def steam_running():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam\ActiveProcess", 0, winreg.KEY_ALL_ACCESS)
    steam_pid = winreg.QueryValueEx(key, "pid")[0]
    winreg.CloseKey(key)
    
    if steam_pid == 0:
        return False

    try:
        process = ps.Process(pid=steam_pid)
        name = process.name()

        if name.lower() == 'steam.exe':
            return True
        else:
            return False
    except ps.NoSuchProcess:
        return False

def get_steamexe_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
        raw_path = winreg.QueryValueEx(key, "SteamExe")[0]
        winreg.CloseKey(key)
        raw_path_items = raw_path.split('/')
        path_items = []
        for item in raw_path_items:
            if ' ' in item:
                path_items.append(f'"{item}"')
            else:
                path_items.append(item)
        steam_exe = "\\".join(path_items)
        return steam_exe
    
    except Exception as e:
        print(f"Error getting Steam path: {e}")
        return None
    
def get_steam_path():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
        raw_path = winreg.QueryValueEx(key, "SteamPath")[0]
        winreg.CloseKey(key)
        raw_path_items = raw_path.split('/')
        path_items = []
        for item in raw_path_items:
            if ' ' in item:
                path_items.append(f'"{item}"')
            else:
                path_items.append(item)
        steam_exe = "\\".join(path_items)
        return steam_exe
    
    except Exception as e:
        print(f"Error getting Steam path: {e}")
        return None


        