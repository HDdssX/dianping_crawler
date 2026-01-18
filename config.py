BASE_URL = 'https://www.dianping.com/'

MAX_PAGES = 5

COMMENT_PAGES = 3

SEARCH_KEYWORD = '轻食'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

COOKIES = {'_lxsdk_cuid': '19bb06b421dc8-093f71ae792b5d8-4c657b58-1ef000-19bb06b421dc8', '_lxsdk': '19bb06b421dc8-093f71ae792b5d8-4c657b58-1ef000-19bb06b421dc8', 'fspop': 'test', '_hc.v': 'f68b0569-9f48-d1d6-9ac6-86b1274bd152.1768285074', 'qruuid': '34b73b75-fbc1-4e12-b306-2cb95911c007', 'dplet': '27e254da255f9fd7ee7d01901af6b9b5', 'dper': '0202c42670856f89ee58fc1ae6587e19f2f9346b020d4de20f45401d07f45f3b576b932feb18e580c46defd53ba28b44c1f1232908b712eb76b400000000d2300000370fc6a1af4b85ab30b9fe7fafff9f33a393e6898b05439134939fa64188b70effb90345d44acbadfdd1c581fad8ea11', 'ua': '%E7%82%B9%E5%B0%8F%E8%AF%844255583750', 'ctu': 'b475189b30deaacd1c653fc3e977384cb537c6ff18801191166d8a8bf86d2143', 's_ViewType': '10', 'cy': '1', 'cye': 'shanghai', 'll': '7fd06e815b796be3df069dec7836c3df', 'PHOENIX_ID': '0a5eec0a-19bc82d8358-1e1aed', 'WEBDFPID': '1zx4xz10w6175u6w03xuux493w1559w280yy93vz58897958wvu1yuy6-1768677046423-1768191599118UWGESMYfd79fef3d01d5e9aadc18ccd4d0c95075594', 'utm_source_rg': 'AM%2588Brbrb%25528'}

CITIES = [
    "Qingdao", "Jinan", "Yantai", "Weifang",
    "Jining", "Taian", "Zibo", "Weihai",
    "Linyi", "Heze", "Dezhou", "Liaocheng",
    "Zaozhuang", "Dongying", "Rizhao", "Binzhou",
]

SCV_FILE_NAME = "light_food_reviews.csv"

FIELDNAMES = ["City", "ShopName", "User", "Score", "Time", "Content"]
