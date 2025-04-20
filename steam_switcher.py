import winreg, subprocess, json, psutil as ps, sys
from time import sleep


def get_config():
    try: 
        with open("config.json", "r") as f:
            return json.load(f)
    except:
        with open("config.json", "w") as f:
            config = {
                "active_account": "",
                "accounts": []
            }
            json.dump(config, f, indent=4)
        return get_config()
    
def setKey(key, value):
    config = get_config()
    config[key] = value
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=4)
    
def getKey(key: str):
    config = get_config()
    return config[key]

def add_account(new_account):
    config = get_config()
    config["accounts"].append(str(new_account))
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Account added")

def del_account(account : list):
    config = get_config()
    accounts  = config["accounts"]
    print(f"Deleting account: {account} ...")
    for i in range(len(accounts)):
        if accounts[i] == account:
            accounts.pop(i)
            break
    with open('config.json', "w") as f:
        json.dump(config, f, indent=4)
    print("Account deleted!")

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

def get_steam_path():
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

def switch_steam_account(username: str):
    try:
        autoLoginUserRef = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
        active_account = winreg.QueryValueEx(autoLoginUserRef, "AutoLoginUser")[0]
        setKey("active_account", active_account)
        if active_account == username:
            print("You alright on this account")
            exit()
        print("Change account from: ", active_account)

        winreg.SetValueEx(autoLoginUserRef, "AutoLoginUser", 0, winreg.REG_SZ, username)
        winreg.CloseKey(autoLoginUserRef)
        setKey("active_account",username)

        if steam_running():
            print("Steam is running") 
            subprocess.run(["start", get_steam_path(), "-shutdown"], shell=True, creationflags=0x08000000, check=True)
            sleep(2)
            counter = 0
            while steam_running():
                if counter <= 10:
                    counter += 1
                    sleep(1)
                    continue
                else:
                    print("Steam still running!")
        

        
        subprocess.run("start steam://open/main",
                   shell=True, check=True)
        print("Launching steam ...")
        sleep(4)
        
        
    except Exception as e:
        print(f"Error switching steam account: {e}")
        


def main(): 
    accounts_list = getKey("accounts")
    curAccount = getKey("active_account")
    print("Current account: " + curAccount)
    if len(sys.argv) == 1:
        pass
    else: 
        if sys.argv[1] in accounts_list:
            switch_steam_account(sys.argv[1])
        elif sys.argv[1] in ("-a", '--add') and sys.argv[2]:
            add_account(sys.argv[2].strip())
        elif sys.argv[1] in ("-d", '--delete') and sys.argv[2]:
            del_account(sys.argv[2].strip())
        elif sys.argv[1] in ("-w", '--write'):
            print("Accounts: " + str(*accounts_list))
        else:
            print("Invalid argument: ", sys.argv)
    

if __name__ == "__main__":
    main()