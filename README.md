# Simple steam switcher account on python
> this steam switcher use cmd arguments for controling

### Install requirements from requirements.txt using:
``` 
pip install -r requirements.txt 
```
### or set them up manually

## Example by application:
``` python steam_switcher.py <account_name> ```
>This command switch account on the written istead <account_name>

### Also you can build application and use it in your projects:
```
pyinstaller --noconfirm --onefile --console --add-data "steam_switcher.py" --paths "venv\Lib\site-packages"  "main.py"
```