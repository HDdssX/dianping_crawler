from playwright.sync_api import sync_playwright
from config import *
import time
import random


def cookies_dict_to_playwright(cookies_dict: dict):
    """
    Convert {"k":"v"} into playwright cookies list.
    Using domain-based cookie is more stable than url-based for cross-subdomains.
    """
    out = []
    for k, v in cookies_dict.items():
        out.append({
            "name": k,
            "value": v,
            "domain": ".dianping.com",
            "path": "/",
        })
    return out


class Crawler:
    def __init__(self):
        self.total_requests = 0
        self.pw = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self, headless: bool = False) -> None:
        self.pw = sync_playwright().start()

        self.browser = self.pw.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
        )

        self.context = self.browser.new_context(
            user_agent=HEADERS["User-Agent"],
            locale="zh-CN",
            viewport={"width": 1366, "height": 768},
        )

        self.context.add_cookies(cookies_dict_to_playwright(COOKIES))

        self.page = self.context.new_page()

        self.page.goto("https://www.dianping.com/", wait_until="domcontentloaded", timeout=20000)
        time.sleep(random.uniform(2, 4))

    def stop(self):
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.pw:
                self.pw.stop()
        except Exception:
            pass

    def _judge_verify(self, html: str) -> bool:
        keywords = ["验证中心", "安全验证", "滑块", "captcha", "verify", "风控"]
        return any(k in html for k in keywords)

    def _anti_ban_sleep(self) -> None:
        self.total_requests += 1
        sleep_time = random.uniform(8, 12)

        if self.total_requests % 15 == 0:
            sleep_time += random.uniform(90, 110)
        elif self.total_requests % 5 == 0:
            sleep_time += random.uniform(20, 40)
        print(f"[-] ANTI-BAN: Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

    def fetch_html(self, url: str, allow_manual=True, timeout_ms: int = 20000, allow_time: int = 30) -> str:
        self._anti_ban_sleep()
        html = ""
        try:
            self.page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            time.sleep(random.uniform(2, 4))
            if self._judge_verify(html):
                if allow_manual and allow_time > 0:
                    print("[!] Detected verification page. Please solve it manually in the opened browser.")
                    input("Press Enter to continue after passing the verification...")
                    html = self.fetch_html(url, allow_manual=False, timeout_ms=timeout_ms, allow_time=allow_time-1)
                else:
                    return None
            else:
                html = self.page.content()
            return html
        except Exception as e:
            print(f"[!] Error when fetching {url}: {e}")

        return None

    def fetch_json(self, url: str, timeout_ms: int = 20000) -> dict:
        self._anti_ban_sleep()

        try:
            resp = self.page.request.get(url, timeout=timeout_ms)
            if resp.status != 200:
                print(f"[!] Error when fetching {url}: Status code {resp.status}")
                return {"error": f"Status code {resp.status}"}
            return resp.json()
        except Exception as e:
            print(f"[!] Error when fetching {url}: {e}")
        return None


crawler = Crawler()