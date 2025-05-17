from steam_switcher import *
import json, subprocess, winreg, sys, os, re


def get_config():
    try: 
        with open("./config.json", "r") as f:
            return json.load(f)
    except:
        with open("./config.json", "w") as f:
            config = {
                "active_account": "",
                "accounts": []
            }
            json.dump(config, f, indent=4)
        return get_config()
    
def get_accounts():
    loginUsersPath = get_steam_path() + "\\config\\loginusers.vdf"
    if (os.path.exists(loginUsersPath)):
        with open(loginUsersPath, "r+", encoding="utf8") as file:
            file_text = file.read()
            accountsName_raw = re.findall(r'"AccountName"\t\t"[\S]{1,}"', file_text)
            file_text = file_text.replace('"AllowAutoLogin"\t\t"0"', '"AllowAutoLogin"\t\t"1"')
                
            file.seek(0)
            file.write(file_text)

        accountsName = [accountName_raw.split("\t\t")[1].replace('"', '') for accountName_raw in accountsName_raw]

        return accountsName
           
def setKey(key, value):
    config = get_config()
    config[key] = value
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=4)
    
def getKey(key: str):
    config = get_config()
    return config[key]


def updateConfig():
    autoLoginUserRef = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
    active_account = winreg.QueryValueEx(autoLoginUserRef, "AutoLoginUser")[0]
    winreg.CloseKey(autoLoginUserRef)
    setKey("active_account", active_account)

    accounts_list = get_accounts()
    setKey("accounts", accounts_list)
    return [active_account, accounts_list]


def switch_steam_account(username: str):
    try:
        autoLoginUserRef = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", 0, winreg.KEY_ALL_ACCESS)
        active_account = winreg.QueryValueEx(autoLoginUserRef, "AutoLoginUser")[0]
        if active_account == username:
            print("You already on this account")
            exit()
        print("Change account from: ", active_account , " to ", username)
        setKey("active_account", active_account)
        winreg.SetValueEx(autoLoginUserRef, "AutoLoginUser", 0, winreg.REG_SZ, username)
        winreg.CloseKey(autoLoginUserRef)

        if steam_running():
            print("Steam is running") 
            subprocess.run(["start", get_steamexe_path(), "-shutdown"], shell=True, creationflags=0x08000000, check=True)
            sleep(2)
            counter = 0
            while steam_running():
                if counter <= 10:
                    counter += 1
                    sleep(1)
                    continue
                else:
                    print("Steam still running!")
        

        
        subprocess.run("start steam://open/main", shell=True, check=True)
        print("Launching steam ...")
        sleep(4)
        
        
        
    except Exception as e:
        print("Error switching steam account:", e)


def main(): 
    active_account, accounts_list = updateConfig()

    if len(sys.argv) == 1:
        print(*accounts_list)
    else: 
        if sys.argv[1] in accounts_list:
            switch_steam_account(sys.argv[1])
        else:
            print("Invalid argument(s): ", *sys.argv)
    

if __name__ == "__main__":
    main()
