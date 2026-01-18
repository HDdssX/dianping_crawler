import re
from bs4 import BeautifulSoup
from urllib.parse import quote
import string
from pw import *
from config import *
import os
import csv
import json

# 查找城市 ID
def find_city_id(city_name: str) -> str:
    req = crawler.fetch_html(BASE_URL + city_name)
    match = re.search(r"cityId\s*=\s*(\d+)", req)
    return match.group(1)


# 搜索获取商户 ID 和名称
def search_for_shop_id(city_id: str, max_pages: int = MAX_PAGES) -> list:
    shop_list = []
    for page in range(1, max_pages + 1):
        print(f"[~] 正在搜索 {city_id} 第 {page} 页商户...")
        url = f"{BASE_URL}search/keyword/{city_id}/0_{SEARCH_KEYWORD}" + (f"/p{page}" if page > 1 else "")
        req = crawler.fetch_html(url)
        soup = BeautifulSoup(req, 'html.parser')
        for a in soup.select("div.tit > a[data-shopid]"):
            shop_name = a.get("title")
            shop_id = a.get("data-shopid")
            if shop_name and shop_id:
                print(f"[+] 找到商户: {shop_name} (ID: {shop_id})")
                shop_list.append({"id": shop_id, "name": shop_name})
    return shop_list


# 通过商户 ID 获取评论
def get_comments(shop_id: str, shop_name: str, max_pages: int = COMMENT_PAGES) -> list:
    comments = []
    for page in range(max_pages):
        url = (
            "https://mapi.dianping.com/mapi/review/outsidesiftedreviewlist.bin"
            "?optimus_code=10&optimus_partner=76&optimus_risk_level=71&reqsource=1"
            "&filterid=800&merge=1&needfilter=1"
            f"&queryid={int(time.time() * 1000)}_{''.join(random.choices(string.ascii_letters, k=random.randint(8, 15)))}&referid={shop_id}&refertype=0&start={page * 14}"
            "&multifilterids=%7B%22filterIds%22:%5B800%5D%7D"
            "&yodaReady=h5&csecplatform=4&csecversion=4.1.1"
        )

        req = crawler.fetch_json(url)

        if "error" in req:
            print(f"[!] Error fetching comments for shop {shop_id}: {req['error']}")
            return [-1]

        if req['list'] is None:
            return comments

        print(f"[*] 正在获取商户 {shop_id} 第 {page + 1} 页评论...")
        for shop_comment in req['list']:
            dic = {
                "ShopName": shop_name,
                "User": shop_comment['feedUser']['userName'],
                "Score": shop_comment['star'],
                "Time": shop_comment['time'],
                "Content": shop_comment['content'].replace("\n", " ")
            }

            if dic not in comments:
                comments.append(dic)
            else:
                return comments

    return comments


if __name__ == "__main__":

    last_failed_city = None
    last_failed_shops = None

    try:
        with open("last_failed_city.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
        last_failed_city = data["last_failed_city"]
        last_failed_shops = data["shops"]
        print(f"[+] Resuming from last failed city: {last_failed_city}")
        if last_failed_city in CITIES:
            for city in CITIES:
                if city == last_failed_city:
                    break
                del CITIES[city]
    except Exception:
        pass

    file_exists = os.path.exists(SCV_FILE_NAME)
    mode = "a" if file_exists else "w"
    with open(SCV_FILE_NAME, mode, encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()

    # url 编码
    SEARCH_KEYWORD = quote(SEARCH_KEYWORD)
    crawler.start(headless=False)


    city_id = {}
    # 获取城市编号
    for city in CITIES:
        city_id[city] = find_city_id(city)
        print(f"[+] {city}: {city_id[city]}")

    for city_name, city_id in city_id.items():
        print(f"\n\n[~] city: {city_name}\n\n")

        if last_failed_shops is not None and last_failed_city is not None:
            shops = last_failed_shops
            del last_failed_shops
            os.remove("last_failed_city.txt")
            print(f"[+] Resuming shop list for city {city_name} from last failure.")
        else:
            shops = search_for_shop_id(city_id)
        print(f"\n[~] Found {len(shops)} shops in {city_name}.\n")

        for i, shop in enumerate(shops):
            print(f"[{i + 1}/{len(shops)}] {shop['name']}\n")
            shop_reviews = get_comments(shop['id'], shop['name'])

            if shop_reviews == [-1]:
                print(f"[!] Stopping further requests for city {city_name} due to error.")
                with open("last_failed_city.txt", "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "city_name": city_name,
                            "shops": shops[i:]
                        },
                        f,
                        ensure_ascii=False
                    )
                    print(f"[+] Recorded last failed city: {city_name}")
                break

            for r in shop_reviews:
                r["City"] = city_name

            with open(SCV_FILE_NAME, "a", encoding="utf-8-sig", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writerows(shop_reviews)

    crawler.stop()
