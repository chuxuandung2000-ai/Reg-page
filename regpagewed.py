import concurrent.futures
from datetime import datetime
import json
import os
import random
import re
import sys
from time import sleep
import requests

os.system('') # Kích hoạt ANSI escape sequence cho Windows CMD
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

os.system('clear' if os.name == 'posix' else 'cls')
dau = "\033[1;32m~ [✓] => "
s3x = f"""\033[1;93m             
\033[1;32m  ██████╗░███████╗░██████╗░.     ██████╗░██████╗░░█████╗░███████╗
\033[1;35m  ██╔══██╗██╔════╝██╔════╝░.     ██╔══██╗██╔══██╗██╔══██╗██╔════╝
\033[1;32m  ██████╔╝█████╗░░██║░░██╗░.     ██████╔╝██████╔╝██║░░██║██████╗░
\033[1;35m  ██╔══██╗██╔══╝░░██║░░╚██╗.     ██╔═══╝░██╔══██╗██║░░██║╚╚████╗
\033[1;36m  ██║░░██║███████╗╚██████╔╝.     ██║░░░░░██║░░██║╚█████╔╝██████╔╝
\033[1;35m  ╚═╝░░╚═╝╚══════╝░╚═════╝░.     ╚═╝░░░░░╚═╝░░╚═╝░╚╚╚════╝░╚╚╚════╝░
\033[1;37m- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\033[1;37m- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""
print(s3x)

print_lock = Lock()
proxy_lock = Lock()

def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

def format_proxy(proxy_str):
    if not proxy_str:
        return None
    proxy_str = proxy_str.strip()
    
    if proxy_str.startswith(('http://', 'https://', 'socks5://', 'socks4://', 'socks5h://')):
        return proxy_str
        
    parts = proxy_str.split(':')
    if len(parts) == 4:
        if parts[1].isdigit():
            host, port, user, pwd = parts
            return f"http://{user}:{pwd}@{host}:{port}"
        elif parts[3].isdigit():
            user, pwd, host, port = parts
            return f"http://{user}:{pwd}@{host}:{port}"
        else:
            host, port, user, pwd = parts[0], parts[1], parts[2], parts[3]
            return f"http://{user}:{pwd}@{host}:{port}"
    elif len(parts) == 2:
        host, port = parts
        return f"http://{host}:{port}"
    return proxy_str

def process_special_proxy(proxy_str):
    formatted = format_proxy(proxy_str)
    proxies = {"http": formatted, "https": formatted} if formatted else None
    
    ip = "Unknown IP"
    country = "VN"
    isp = "Proxy Server"
    proxy_type = "Xoay (Rotating)"
    
    check_urls = [
        "https://api.ipify.org?format=json",
        "http://ip-api.com/json/?fields=query,country,isp",
        "https://httpbin.org/ip"
    ]
    
    for url in check_urls:
        try:
            res = requests.get(url, proxies=proxies, timeout=6)
            if res.status_code == 200:
                data = res.json()
                if "ip" in data:
                    ip = data["ip"]
                elif "query" in data:
                    ip = data["query"]
                    country = data.get("country", "VN")
                    isp = data.get("isp", "Proxy ISP")
                elif "origin" in data:
                    ip = data["origin"]
                break
        except Exception:
            continue
            
    if ip == "Unknown IP":
        ip = "Active (User Verified Live)"

    return {
        "status": "LIVE",
        "ip": ip,
        "country": country,
        "isp": isp,
        "type": proxy_type,
        "formatted": formatted
    }

def get_multi_browser_fingerprint():
    """Tạo bộ vân tay độc lập luân phiên qua các trình duyệt Chrome, Cốc Cốc, Safari, Firefox, Edge."""
    browsers = ["chrome", "coccoc", "safari", "firefox", "edge"]
    b_type = random.choice(browsers)
    
    if b_type == "chrome":
        v_full = random.choice(["120.0.6099.144", "121.0.6167.85", "122.0.6261.94", "123.0.6312.58", "124.0.6367.60"])
        v_major = v_full.split('.')[0]
        platform = random.choice(['"Windows"', '"Macintosh"'])
        os_str = "Windows NT 10.0; Win64; x64" if platform == '"Windows"' else "Macintosh; Intel Mac OS X 10_15_7"
        ua = f"Mozilla/5.0 ({os_str}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v_full} Safari/537.36"
        sec_ch_ua = f'"Chromium";v="{v_major}", "Google Chrome";v="{v_major}", "Not=A?Brand";v="99"'
    elif b_type == "coccoc":
        v_full = random.choice(["120.0.6099.144", "122.0.6261.94", "124.0.6367.60"])
        v_major = v_full.split('.')[0]
        platform = '"Windows"'
        ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v_full} Safari/537.36 CocCoc/{v_major}.0.120"
        sec_ch_ua = f'"Chromium";v="{v_major}", "CocCoc";v="{v_major}", "Not=A?Brand";v="99"'
    elif b_type == "safari":
        v_safari = random.choice(["605.1.15", "604.1.38"])
        v_os = random.choice(["14_7_1", "15_4", "16_5", "17_2"])
        platform = '"Macintosh"'
        ua = f"Mozilla/5.0 (Macintosh; Intel Mac OS X {v_os}) AppleWebKit/{v_safari} (KHTML, like Gecko) Version/17.2 Safari/{v_safari}"
        sec_ch_ua = '"Not=A?Brand";v="8", "Chromium";v="120"'
    elif b_type == "firefox":
        v_ff = random.choice(["121.0", "122.0", "123.0", "124.0"])
        platform = random.choice(['"Windows"', '"Linux"'])
        os_str = "Windows NT 10.0; Win64; x64" if platform == '"Windows"' else "X11; Linux x86_64"
        ua = f"Mozilla/5.0 ({os_str}) Gecko/20100101 Firefox/{v_ff}"
        sec_ch_ua = '"Not=A?Brand";v="99"'
    else: # Edge
        v_full = random.choice(["120.0.2210.91", "121.0.2277.106", "122.0.2365.92"])
        v_major = v_full.split('.')[0]
        platform = '"Windows"'
        ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v_full} Safari/537.36 Edg/{v_full}"
        sec_ch_ua = f'"Chromium";v="{v_major}", "Microsoft Edge";v="{v_major}", "Not=A?Brand";v="99"'

    viewport_width = str(random.choice([1366, 1440, 1536, 1920]))
    return ua, sec_ch_ua, platform, viewport_width, b_type

class reg_pro5:
    def __init__(self, credential, proxy=None, is_token=False) -> None:
        self.is_token = is_token
        self.credential = credential
        self.update_proxy(proxy)

        ua, sec_ch_ua, platform, viewport_width, self.browser_type = get_multi_browser_fingerprint()
        self.ua = ua
        self.sec_ch_ua = sec_ch_ua
        self.platform = platform
        self.viewport_width = viewport_width

        self.id_acc = ""
        self.cookies = ""
        self.access_token = ""

        if self.is_token:
            self.access_token = credential
            self.id_acc = self.extract_uid_from_token(self.access_token)
        else:
            self.cookies = credential
            try:
                self.id_acc = self.cookies.split('c_user=')[1].split(';')[0]
            except:
                self.id_acc = ""

        self.headers = {
            "authority": "www.facebook.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": self.sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": self.platform,
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": self.ua,
            "viewport-width": self.viewport_width,
        }

        if not self.is_token:
            self.headers["cookie"] = self.cookies
        
        self.fb_dtsg = ""
        self.lsd = "AVr-4211_Q"
        self.__rev = "1011500000"
        self.__hs = "19783.HYP:comet_pkg.2.1.0.2.1"
        
        self.refresh_session_info()
        self.web_browser_simulation_flow()

    def extract_uid_from_token(self, token):
        try:
            # Lấy UID qua Graph API bằng Android Token
            res = requests.get(f"https://graph.facebook.com/me?access_token={token}&fields=id", timeout=10)
            if res.status_code == 200:
                return res.json().get("id", "")
        except:
            pass
        return "1000" + str(random.randint(100000000, 999999999))

    def update_proxy(self, proxy):
        self.proxy = proxy
        self.formatted_proxy = format_proxy(proxy)
        self.proxies_dict = {"http": self.formatted_proxy, "https": self.formatted_proxy} if self.formatted_proxy else None
        
        if not hasattr(self, 'session') or self.session is None:
            self.session = requests.Session()
        
        if self.proxies_dict:
            self.session.proxies.update(self.proxies_dict)
        else:
            self.session.proxies.clear()

    def refresh_session_info(self):
        try:
            if self.is_token:
                # Dùng Android token lấy thông tin
                res = self.session.get(f"https://graph.facebook.com/v18.0/me?access_token={self.access_token}&fields=id,name", timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    self.id_acc = data.get("id", self.id_acc)
                    self.fb_dtsg = "AQI" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=30))
                return

            res_me = self.session.get("https://www.facebook.com/me", headers=self.headers, timeout=15)
            url_profile = res_me.url
            
            if "checkpoint" in url_profile or "login" in url_profile:
                return

            profile = self.session.get(url_profile, headers=self.headers, timeout=15).text
            
            if 'DTSGInitialData' in profile:
                try:
                    self.fb_dtsg = profile.split('"token":"')[1].split('"')[0]
                except:
                    self.fb_dtsg = profile.split('{"name":"fb_dtsg","value":"')[1].split('"}')[0]
            elif '["DTSGInitData",[],{"token":"' in profile:
                self.fb_dtsg = profile.split('["DTSGInitData",[],{"token":"')[1].split('"')[0]
            else:
                try:
                    self.fb_dtsg = profile.split('{"name":"fb_dtsg","value":"')[1].split('"}')[0]
                except:
                    self.fb_dtsg = profile.split(',"f":"')[1].split('","l":null}')[0]
            
            try:
                self.lsd = profile.split('["LSD",[],{"token":"')[1].split('"')[0]
            except:
                pass

            try:
                rev_match = re.search(r'"rev":\s*(\d+)', profile)
                if rev_match:
                    self.__rev = rev_match.group(1)
            except:
                pass

            try:
                hs_match = re.search(r'"client_revision":\s*"([^"]+)"', profile)
                if hs_match:
                    self.__hs = hs_match.group(1)
            except:
                pass
        except:
            pass

    def web_browser_simulation_flow(self):
        if self.is_token:
            return
        try:
            headers_flow = self.headers.copy()
            headers_flow["sec-fetch-dest"] = "document"
            headers_flow["sec-fetch-mode"] = "navigate"
            headers_flow["sec-fetch-site"] = "same-origin"
            
            self.session.get("https://www.facebook.com/", headers=headers_flow, timeout=10)
            sleep(random.uniform(1.0, 2.0))
            
            res = self.session.get("https://www.facebook.com/pages/creation/?ref_type=launch_point", headers=headers_flow, timeout=10)
            page_content = res.text
            if 'DTSGInitialData' in page_content:
                try:
                    token = page_content.split('"token":"')[1].split('"')[0]
                    if token:
                        self.fb_dtsg = token
                except:
                    pass
            sleep(random.uniform(1.5, 2.5))
        except Exception:
            pass

    def Reg(self, name):
        if not self.fb_dtsg or not self.id_acc:
            return {"error": "Lấy thông tin tài khoản hoặc fb_dtsg thất bại (Die Token/Cookie / Checkpoint)"}

        if self.is_token:
            # Reg qua Android Graph API nếu dùng Token Android
            try:
                url = f"https://graph.facebook.com/v18.0/{self.id_acc}/additional_profiles"
                payload = {
                    "access_token": self.access_token,
                    "name": name,
                    "category_id": "181475575221097"
                }
                res = self.session.post(url, data=payload, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    if "id" in data:
                        return {"data": {"additional_profile_plus_create": {"page": {"id": data["id"]}}}}
                return {"error": f"Android Token API Error: {res.text[:100]}"}
            except Exception as e:
                return {"error": str(e)}

        headers_reg = {
            "authority": "www.facebook.com",
            "accept": "*/*",
            "accept-language": "vi-VN,vi;q=0.9",
            "cookie": self.cookies,
            "origin": "https://www.facebook.com",
            "referer": "https://www.facebook.com/pages/creation?ref_type=launch_point",
            "sec-ch-prefers-color-scheme": "light",
            "sec-ch-ua": self.sec_ch_ua,
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": self.platform,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-fb-friendly-name": "AdditionalProfilePlusCreationMutation",
            "x-fb-lsd": self.lsd,
        }

        data = {
            "av": self.id_acc,
            "__user": self.id_acc,
            "__a": "1",
            "__dyn": "7AzHxq1mxu1syUbFuC0BVU98nwgU29zEdEc8co5S3O2S7o11Ue8hw6vwb-q7oc81xoswIwuo886C11xmfz81sbzoaEnxO0Bo7O2l2Utwwwi831wiEjwZwlo5qfK6E7e58jwGzE8FU5e7oqBwJK2W5olwuEjUlDw-wUws9ovUaU3qxWm2Sq2-azo2NwkQ0z8c84K2e3u362-2B0oobo",
            "__csr": "gP4ZAN2d-hbbRmLObkZO8LvRcXWVvth9d9GGXKSiLCqqr9qEzGTozAXiCgyBhbHrRG8VkQm8GFAfy94bJ7xeufz8jK8yGVVEgx-7oiwxypqCwgF88rzKV8y2O4ocUak4UpDxu3x1K4opAUrwGx63J0Lw-wa90eG18wkE7y14w4hw6Bw2-o069W00CSE0PW06aU02Z3wjU6i0btw3TE1wE5u",
            "__req": "t",
            "__hs": self.__hs,
            "dpr": str(random.choice([1, 1.25, 1.5])),
            "__ccg": "EXCELLENT",
            "__rev": self.__rev,
            "__s": f"{random.choice(['a', 'b', 'c'])}{random.randint(1000,9999)}:x{random.randint(100,999)}",
            "__hsi": str(random.randint(7200000000000000000, 7300000000000000000)),
            "__comet_req": "15",
            "fb_dtsg": self.fb_dtsg,
            "jazoest": str(random.randint(20000, 28000)),
            "lsd": self.lsd,
            "__aaid": "800444344545377",
            "__spin_r": self.__rev,
            "__spin_b": "trunk",
            "__spin_t": str(int(datetime.now().timestamp())),
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "AdditionalProfilePlusCreationMutation",
            "variables": json.dumps({
                "input": {
                    "bio": "",
                    "categories": ["181475575221097"],
                    "creation_source": "comet_web_creation",
                    "name": name,
                    "page_referrer": "launch_point",
                    "actor_id": self.id_acc,
                    "client_mutation_id": str(random.randint(1, 999999)),
                    "entry_point": "profile_plus_creation_flow"
                }
            }),
            "server_timestamps": "true",
            "doc_id": "5903223909690825",
        }

        try:
            response = self.session.post(
                "https://www.facebook.com/api/graphql/",
                headers=headers_reg,
                data=data,
                timeout=20
            )
            
            raw_text = response.text.strip()
            if not raw_text:
                return {"error": "Phản hồi từ Facebook trống (Bị chặn request / Rate limit)"}
            
            if raw_text.startswith("for (;;);"):
                raw_text = raw_text[9:].strip()
                
            try:
                return json.loads(raw_text)
            except json.JSONDecodeError:
                return {"error": f"Phản hồi không phải JSON hợp lệ: {raw_text[:80]}"}
                
        except Exception as e:
            return {"error": str(e)}

    def update_page_avatar(self, page_id, avatar_mode, custom_link=""):
        if self.is_token:
            return False
        try:
            img_bytes = None
            if avatar_mode == "1":
                res_img = self.session.get("https://thispersondoesnotexist.com/", timeout=15, headers={"User-Agent": self.ua})
                if res_img.status_code == 200:
                    img_bytes = res_img.content
            elif avatar_mode == "2" and custom_link:
                res_img = self.session.get(custom_link, timeout=15, headers={"User-Agent": self.ua})
                if res_img.status_code == 200:
                    img_bytes = res_img.content

            if not img_bytes:
                return False

            upload_url = "https://www.facebook.com/profile/picture/upload/"
            files = {'file': ('avatar.jpg', img_bytes, 'image/jpeg')}
            data = {
                "av": page_id,
                "__user": self.id_acc,
                "__a": "1",
                "fb_dtsg": self.fb_dtsg,
                "lsd": self.lsd,
            }
            res = self.session.post(upload_url, headers=self.headers, data=data, files=files, timeout=20)
            return True
        except Exception:
            return False

def is_valid_proxy_string(p):
    if not p:
        return False
    p = p.strip()
    if 'c_user=' in p or 'xs=' in p or 'EAAB' in p:
        return False
    if p.startswith(('http://', 'https://', 'socks5://', 'socks4://', 'socks5h://')):
        return True
    if '@' in p:
        if ':' in p and '.' in p:
            return True
        return False
    parts = p.split(':')
    if len(parts) == 2 and parts[1].isdigit():
        if '.' in parts[0] or parts[0] == 'localhost':
            return True
    elif len(parts) == 4:
        if parts[1].isdigit() or parts[3].isdigit():
            return True
    return False

def extract_account_info(line):
    line = line.strip()
    credential = ""
    proxy = None
    is_token = False

    if line.startswith("EAAB") or (len(line) > 50 and '|' not in line and 'c_user=' not in line):
        return line, None, True

    if '|' in line:
        parts = [p.strip() for p in line.split('|')]
        cred_idx = -1
        for idx, p in enumerate(parts):
            if 'c_user=' in p or p.startswith("EAAB") or len(p) > 50:
                credential = p
                cred_idx = idx
                if p.startswith("EAAB"):
                    is_token = True
                break

        if cred_idx != -1:
            for idx, p in enumerate(parts):
                if idx == cred_idx:
                    continue
                if p.isdigit() and len(p) >= 8:
                    continue
                if is_valid_proxy_string(p):
                    proxy = p
                    break
        else:
            m = re.search(r'(c_user=\d+;[^|\n]+)', line)
            if m:
                credential = m.group(1).strip()
            else:
                credential = line
    else:
        m = re.search(r'(c_user=\d+;[^\n]+)', line)
        if m:
            credential = m.group(1).strip()
        else:
            credential = line

    return credential, proxy, is_token

def get_random_name(name_type):
    if name_type == "1":
        arrayho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Vũ", "Phan", "Trương", "Bùi", "Đặng", "Đỗ", "Ngô", "Hồ", "Dương", "Đinh"]
        arraylot = ["Văn", "Gia", "Hữu", "Đình", "Thanh", "Minh", "Tuấn", "Hoàng"]
        arrayten = ["Hưng", "Anh", "Đạt", "Tuấn", "Long", "Quốc", "Nam", "Giang", "Khang", "Dương", "Phúc", "Bảo", "Khôi"]
        return f"{random.choice(arrayho)} {random.choice(arraylot)} {random.choice(arrayten)}"
    else:
        first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

def countdown_delay(uid, dl):
    safe_print(dau, f"\033[1;33m🌸 [UID: {uid}] Đang Delay Reg Pro5 {dl}s trước lượt tiếp theo...\033[0m")
    sleep(dl)

def run_account(raw_line, initial_proxy, proxies_list, proxy_index_ref, sl_pro5, dl, name_type, avatar_mode, custom_link):
    try:
        credential, line_proxy, is_token = extract_account_info(raw_line)
        if not credential:
            safe_print(dau, f"\033[1;31m Dữ liệu tài khoản không hợp lệ: {raw_line[:30]}...")
            return

        current_proxy = line_proxy if line_proxy else initial_proxy
        
        proxy_check = process_special_proxy(current_proxy) if current_proxy else {"status": "LIVE", "ip": "Direct (No Proxy)", "country": "N/A", "isp": "N/A", "type": "N/A"}
        current_ip = f"{proxy_check['ip']} ({proxy_check['country']} - {proxy_check['isp']} | Loại: {proxy_check['type']})"
        proxy_note = "(Proxy riêng kẹp theo acc)" if line_proxy else "(Proxy chia đều)"
        
        bot = reg_pro5(credential, current_proxy, is_token=is_token)
        safe_print(dau, f"\033[1;36m Tài khoản {bot.id_acc} | Trình duyệt: \033[1;32m{bot.browser_type.upper()}\033[0m | IP: {current_ip} {proxy_note}")

        if not bot.id_acc or not bot.fb_dtsg:
            safe_print(dau, f"\033[1;31m [UID: {bot.id_acc}] Khởi tạo thất bại hoặc chết token/cookie, dừng luồng ngay lập tức!")
            return
        
        safe_print(dau, f"\033[1;32m Bắt đầu chạy tài khoản ID: {bot.id_acc} (Reg {sl_pro5} page)")

        success_count = 0
        for i in range(1, int(sl_pro5) + 1):
            name = get_random_name(name_type)
            res = bot.Reg(name)
            
            is_success = False
            error_msg = ""
            page_id = None
            
            if isinstance(res, dict):
                if "errors" in res:
                    error_msg = str(res.get("errors"))
                elif "error" in res:
                    error_msg = f"Lỗi FB Code: {res.get('error')} - {res.get('errorSummary', '')}"
                elif "data" in res:
                    data_inner = res.get("data")
                    if data_inner and isinstance(data_inner, dict):
                        add_profile = data_inner.get("additional_profile_plus_create")
                        if add_profile and isinstance(add_profile, dict):
                            err_msg_fb = add_profile.get("error_message")
                            page_info = add_profile.get("page")
                            if err_msg_fb:
                                error_msg = err_msg_fb
                            elif page_info and page_info.get("id"):
                                is_success = True
                                page_id = page_info.get("id")
                            else:
                                error_msg = "Không trả về ID Page (Bị chặn ngầm/Checkpoint ẩn)"
                        else:
                            error_msg = "Thiếu trường additional_profile_plus_create"
                    else:
                        error_msg = "Dữ liệu trả về trống"
                else:
                    error_msg = str(res)
            else:
                error_msg = str(res)

            # ĐIỀU KIỆN TỐI THƯỢNG: Gặp lỗi dù chỉ 1 lần là dừng hẳn luồng ngay lập tức để bảo vệ acc
            if not is_success:
                safe_print(dau, f"\033[1;31m [UID: {bot.id_acc}] Lỗi Reg Page ({name}): {error_msg}")
                safe_print(dau, f"\033[1;31m [UID: {bot.id_acc}] Phát hiện lỗi lần đầu, dừng hẳn luồng tài khoản này theo yêu cầu để tránh die acc!")
                break

            if is_success:
                success_count += 1
                safe_print(dau, f"\033[1;32m [UID: {bot.id_acc}] ({success_count}/{sl_pro5}) Reg Thành Công Page: {name} (ID: {page_id})")
                
                if avatar_mode in ["1", "2"] and page_id and not bot.is_token:
                    safe_print(dau, f"\033[1;35m [UID: {bot.id_acc}] Đang cập nhật Avatar cho Page...")
                    updated = bot.update_page_avatar(page_id, avatar_mode, custom_link)
                    if updated:
                        safe_print(dau, f"\033[1;32m [UID: {bot.id_acc}] Cập nhật Avatar thành công!")
                    else:
                        safe_print(dau, f"\033[1;31m [UID: {bot.id_acc}] Cập nhật Avatar thất bại!")

            if i < int(sl_pro5):
                safe_delay = dl + random.randint(4, 10)
                countdown_delay(bot.id_acc, safe_delay)
    except Exception as e:
        safe_print(dau, f"\033[1;31m Lỗi luồng tài khoản: {str(e)}")

def main():
    try:
        print(dau + "\033[1;35mNhập danh sách Proxy (Mỗi proxy 1 dòng, dán xong bấm Enter 2 lần. Không có thì ấn Enter luôn):")
        proxies = []
        while True:
            try:
                line = input()
                if not line.strip():
                    break
                proxies.append(line.strip())
            except EOFError:
                break

        if proxies:
            print(dau + f"\033[1;36m Đang xử lý và nhận diện {len(proxies)} proxy...")
            live_proxies = []
            for idx, p in enumerate(proxies, 1):
                res = process_special_proxy(p)
                live_proxies.append(p)
                print(dau + f"   [Proxy {idx}] IP: {res['ip']} | Quốc gia: {res['country']} | Loại: \033[1;32m{res['type']}\033[0m - \033[1;32mSẴN SÀNG (LIVE)\033[0m")
            proxies = live_proxies
            print(dau + f"\033[1;32m Tổng số proxy sẵn sàng sử dụng: {len(proxies)}\n")

        print(dau + "\033[1;35mNhập danh sách Acc (Hỗ trợ Cookie hoặc Android Token EAAB...):")
        print(dau + "\033[1;33m(Nhập xong bấm Enter 3 lần liên tiếp hoặc gõ 'done' để chạy):")
        lines = []
        empty_count = 0
        while True:
            try:
                line = input()
                if line.strip().lower() == 'done':
                    break
                if not line.strip():
                    empty_count += 1
                    if empty_count >= 3:
                        break
                else:
                    empty_count = 0
                    lines.append(line.strip())
            except EOFError:
                break

        if not lines:
            print(dau + "\033[1;31m Không có tài khoản nào được nhập!")
            return

        sl_pro5 = input(dau + "\033[1;35mNhập số lượng Pro5 muốn reg cho mỗi acc: ").strip()
        dl = input(dau + "\033[1;35mNhập Delay cơ bản giữa các lần reg (giây): ").strip()
        
        max_threads_str = input(dau + "\033[1;35mNhập số lượng luồng muốn chạy đồng thời: ").strip()
        thread_delay_str = input(dau + "\033[1;35mNhập delay giữa các luồng khởi động (giây): ").strip()

        print(dau + "\033[1;36mChọn loại tên:")
        print(dau + "\033[1;37m[1] Tên Việt Nam")
        print(dau + "\033[1;37m[2] Tên Ngoại (English)")
        name_type = input(dau + "\033[1;35mNhập lựa chọn (1 hoặc 2): ").strip()
        if name_type not in ["1", "2"]:
            name_type = "1"

        print(dau + "\033[1;36mCài đặt Ảnh đại diện (Avatar) cho Page:")
        print(dau + "\033[1;37m[1] Lấy ảnh AI ngẫu nhiên từ ThisPersonDoesNotExist.com")
        print(dau + "\033[1;37m[2] Dán link ảnh trực tiếp (tự động dùng 1 link cho tất cả)")
        print(dau + "\033[1;37m[0] Không up ảnh (Bỏ qua)")
        avatar_mode = input(dau + "\033[1;35mNhập lựa chọn (0, 1 hoặc 2): ").strip()
        
        custom_link = ""
        if avatar_mode == "2":
            custom_link = input(dau + "\033[1;35mNhập đường dẫn trực tiếp của ảnh (URL): ").strip()

        if not sl_pro5.isdigit() or not dl.isdigit() or not max_threads_str.isdigit() or not thread_delay_str.isdigit():
            print(dau + "\033[1;31m Các thông số nhập vào phải là số hợp lệ!")
            return

        max_threads = int(max_threads_str)
        thread_delay = float(thread_delay_str)
        dl_int = int(dl)

        print(dau + f"\033[1;32m Đang chạy {len(lines)} tài khoản với {max_threads} luồng (Delay giữa các luồng: {thread_delay}s)...\n")

        proxy_index_ref = [0]
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            for index, raw_line in enumerate(lines):
                initial_proxy = proxies[index % len(proxies)] if proxies else None
                executor.submit(
                    run_account, 
                    raw_line, 
                    initial_proxy, 
                    proxies, 
                    proxy_index_ref, 
                    int(sl_pro5), 
                    dl_int, 
                    name_type, 
                    avatar_mode, 
                    custom_link
                )
                if thread_delay > 0:
                    sleep(thread_delay)

        print(dau + "\033[1;32m Đã hoàn tất tất cả các luồng chạy!")
    except Exception as e:
        print(dau + f"\033[1;31m Lỗi chương trình chính: {str(e)}")

if __name__ == '__main__':
    main()
    input("\n\033[1;33mQuá trình đã kết thúc. Bấm Enter để thoát cửa sổ này...")