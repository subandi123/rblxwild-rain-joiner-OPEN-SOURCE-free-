import ctypes
import os
import re
import shutil
import ssl
import threading
import time

import json
import zipfile
from io import BytesIO

import requests
from colorama import Fore
from playwright.sync_api import sync_playwright
from websocket import WebSocketApp, WebSocketException
import cloudscraper
import pygetwindow as gw

zz = []


def banner():
    os.system("cls")
    print(Fore.LIGHTBLUE_EX + "              ,--.           ,--.       ,--.                      ".center(
        shutil.get_terminal_size().columns))
    print(Fore.LIGHTBLUE_EX + ",--.--.,--,--.`--',--,--,    `--' ,---. `--',--,--, ,---. ,--.--. ".center(
        shutil.get_terminal_size().columns))
    print(Fore.LIGHTBLUE_EX + "|  .--' ,-.  |,--.|      \   ,--.| .-. |,--.|      \ .-. :|  .--' ".center(
        shutil.get_terminal_size().columns))
    print(Fore.LIGHTBLUE_EX + "|  |  \ '-'  ||  ||  ||  |   |  |' '-' '|  ||  ||  \   --.|  |    ".center(
        shutil.get_terminal_size().columns))
    print(Fore.LIGHTBLUE_EX + "`--'   `--`--'`--'`--''--' .-'  / `---' `--'`--''--'`----'`--'   ".center(
        shutil.get_terminal_size().columns))
    print(Fore.BLUE + "AUTO JOIN. By: nonamebetoo#6403".center(shutil.get_terminal_size().columns))


banner()


def information(text):
    print(
        f"({Fore.BLACK}~{Fore.RESET}) {Fore.GREEN}{text}"
    )


def rain(text, content=None):
    print(
        f"({Fore.LIGHTGREEN_EX}${Fore.GREEN}) {text}{' > ' + content if content else ''}"
    )


def error(text, content=None):
    print(
        f"({Fore.LIGHTRED_EX}-{Fore.RESET}) {Fore.LIGHTRED_EX}{text}{Fore.RED}{' > ' + content if content else ''}"
    )


def joinedplayer(text):
    print(
        f"({Fore.BLACK}{Fore.RESET}) {Fore.RED}{text}"
    )


def keepalive(ws):
    while True:
        try:
            ws.send(f'42["time:requestSync",{{"clientTime":{time.time()}}}]')
            time.sleep(3)
        except:
            try:
                ws.close()
            except:
                pass
            break


def strip_msg(message):
    try:
        return json.loads(re.sub(r'\d+\{', '{', message))
    except:
        return json.loads(re.sub(r'\d+\[', '[', message))


def checkusername(auth):
    user_data = None

    def on_message(ws, msgs):
        nonlocal user_data
        msg = strip_msg(msgs)
        if "pingInterval" in msgs:
            ws.send("40")
            time.sleep(3)
            ws.send(f'42["authentication",{{"authToken":"{auth}","clientTime":{time.time()}}}]')
        elif type(msg) is list and msg[0] == "authenticationResponse":
            user_data = msg[1]["userData"]["displayName"]
            ws.close()

    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US',
        'Cache-Control': 'no-cache',
        'Connection': 'Upgrade',
        'Pragma': 'no-cache',
        'Upgrade': 'websocket',
        'Cookie': '__mmapiwsid=136d1c26-58d5-4b5a-9510-24ae84923789:793c4253d9f40c54143f821e27ef22ec734e3d47; cf_clearance=BND6vYteUaghnx2HFqcFqPisIpx88F3dwVYJQHiM0uA-1676409998-0-160; _gcl_au=1.1.322595681.1687039359; session=s%3AfTUpLvTD7uRMLwb1Vl43i2e0W5dD273n.5htyzo2DK%2Bt9j7w%2FTGAkrEleJb7yaM6VELEEmzfh%2B2w',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    while True:
        try:
            wsa = WebSocketApp("wss://rblxwild.com/socket.io/?EIO=4&transport=websocket", header=headers,
                               on_message=on_message)
            wsa.run_forever()
            return user_data
        except WebSocketException as e:
            print(f'WebSocket exception: {e}')
            return None


def joinrain(authtoken, token, potid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Authorization": authtoken,
        "Origin": "https://rblxwild.com",
        "DNT": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "TE": "trailers"
    }

    cookies = {
        "session": "s%3Ayj8YfYb5_J8zywf8Mc5jrVKOamk150BW.jOFzFWedsGSsnn%2FNYWT%2BqnH%2Br%2FN0B5248gcZ0ynpZNY"
    }

    json = {
        "captchaToken": token,
        "potId": potid,
        "i1oveu": True
    }

    try:
        response = requests.post("https://rblxwild.com/api/events/rain/join", json=json, headers=headers,
                                 cookies=cookies)
    except Exception as e:
        print(e)
        return False
    else:
        if response.json()['success']:
            joinedplayer(f'Joined on account: {checkusername(authtoken)}')
        else:
            joinedplayer(f'Not Joined on account: : {checkusername(authtoken)}')


def on_message(ws, msgs):
    msg = strip_msg(msgs)
    global rainAmount
    global pot_id
    if "pingInterval" in msgs:
        threading.Thread(target=keepalive, args=(ws,)).start()

    elif type(msg) is list and msg[0] == "authenticationResponse":
        pot_id = msg[1]["events"]["rain"]["pot"]["id"]

    elif type(msg) is list and msg[0] == "events:rain:updatePotVariables":
        rainAmount = msg[1]["newPrize"]

    elif type(msg) is list and msg[0] == "events:rain:setState":
        if msg[1]["newState"] == "ENDING":
            rain(f'Joining Rain With Amount - {rainAmount} -')
            with open("config.json", "r+") as data:
                config = json.load(data)
                auth = config["authorization"]
                for i in range(len(auth)):
                    a = auth[i]
                    b = zz[i]
                    c = pot_id
                    d = b['token']
                    threading.Thread(target=joinrain, args=(a, d, c)).start()
        elif msg[1]["newState"] == "ENDED":
            pot_id += 1
            information("Rain ended!")


def on_open(_):
    information("Connected")
    time.sleep(1)
    _.send("40")
    time.sleep(3)
    _.send(f'42["authentication",{{"authToken":"{None}","clientTime":{time.time()}}}]')
    time.sleep(1)
    channel = "EN"
    json_str = f'42["chat:subscribe",{{"channel":"{channel}"}}]'
    _.send(json_str)


def on_err(_, err):
    error("error", err)


headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US',
    'Cache-Control': 'no-cache',
    'Connection': 'Upgrade',
    'Pragma': 'no-cache',
    'Upgrade': 'websocket',
    'Cookie': '__mmapiwsid=136d1c26-58d5-4b5a-9510-24ae84923789:793c4253d9f40c54143f821e27ef22ec734e3d47; cf_clearance=BND6vYteUaghnx2HFqcFqPisIpx88F3dwVYJQHiM0uA-1676409998-0-160; _gcl_au=1.1.322595681.1687039359; session=s%3AfTUpLvTD7uRMLwb1Vl43i2e0W5dD273n.5htyzo2DK%2Bt9j7w%2FTGAkrEleJb7yaM6VELEEmzfh%2B2w',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}


def thehektcaptha():
    url = 'https://github.com/Wikidepia/hektCaptcha-extension/releases/download/v0.2.9/hektCaptcha-v0.2.9.chrome.zip'

    response = requests.get(url, allow_redirects=True)

    z = zipfile.ZipFile(BytesIO(response.content))
    z.extractall(os.path.join(os.getenv('TEMP'), 'hektCaptcha-v0.2.9'))


def start():
    while True:
        try:
            wsa = WebSocketApp("wss://rblxwild.com/socket.io/?EIO=4&transport=websocket", header=headers,
                               on_open=on_open, on_message=on_message, on_error=on_err)
            wsa.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, origin="https://rblxwild.com", host="rblxwild.com",
                            reconnect=True)
        except WebSocketException as e:
            error(f'here websocket except error {e}')
            time.sleep(3)
            continue


def checknumberthatneedtoopen():
    with open("config.json", "r+") as data:
        config = json.load(data)
        lol = config['hcaptcha']['howmanyshouldweopen']
        return lol


def registration():
    with sync_playwright() as pw:
        extension_path = os.path.join(os.getenv('TEMP'), 'hektCaptcha-v0.2.9')
        browser = pw.chromium.launch_persistent_context(
            "",
            headless=False,  ##extension dont work with headless
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )
        lol = browser.new_page()
        lol.set_viewport_size({"width": 1, "height": 1})
        while True:
            try:
                lol.goto("https://hcaptcha.projecttac.com/?sitekey=30a8dcf5-481e-40d1-88de-51ad22aa8e97")

                try:
                    lol.wait_for_function(
                        "() => document.querySelector('[data-hcaptcha-response]').getAttribute('data-hcaptcha-response') !== ''",
                        timeout=40000)
                except TimeoutError:
                    print("eh")

                element = lol.query_selector('[data-hcaptcha-response]')
                response_value = element.get_attribute('data-hcaptcha-response')
                zz.append({"token": response_value, "time": time.time()})
            except Exception as e:
                pass


def cleanup_tokens():
    while True:
        current_time = time.time()
        for token in zz[:]:
            if current_time - token["time"] > 120:
                zz.remove(token)
        time.sleep(1)


threading.Thread(target=start).start()
threading.Thread(target=cleanup_tokens).start()
for i in range(checknumberthatneedtoopen()):
    thread = threading.Thread(target=registration)
    thread.start()
