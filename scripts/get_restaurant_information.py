"""抓取亞洲大學周邊餐廳菜單 (QuickClick LINE 商店 API)。

執行後將所有店家的菜單與價格彙整為一份 CSV,
營養成分需另行人工整理後併入 data/restaurant_information_v3.csv。
"""
import requests
import pandas as pd

# 各餐廳於 QuickClick 平台上的帳號編號
SHOPS = {
    'We Tea': 22492,
    '好義式': 19859,
    '呷飽寶 飯盒/麵食': 19236,
    '艾旦咖哩坊': 15489,
    '樂享鍋物': 15183,
    '四喜壽喜、夏威夷輕食': 15147,
    '食在好味自助餐': 3209,
    '鍋來粥到': 3167,
    '麥味登亞大地餐店': 3153,
    '八方雲集 亞洲大學店': 3142,
    '美而美早餐 亞大店': 3141,
    '嗑吧韓式料理 亞大店': 3140,
}

HEADERS = {
    'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

OUTPUT_CSV = 'restaurant_menus_raw.csv'


def fetch_menu(account_id):
    url = f'https://line.quickclick.cc/line/system/accounts/{account_id}/products'
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def process_menu(json_data, shop_name):
    rows = []
    for category in json_data:
        for product in category['products']:
            rows.append({
                '商店名稱': shop_name,
                '品項': category['categoryName'],
                '菜單': product['productName'],
                '價格': product['productAmount'],
            })
    return rows


def main():
    all_rows = []
    for shop_name, account_id in SHOPS.items():
        try:
            json_data = fetch_menu(account_id)
            rows = process_menu(json_data, shop_name)
            all_rows.extend(rows)
            print(f'{shop_name}: {len(rows)} 筆')
        except Exception as e:
            print(f'{shop_name}: 抓取失敗 - {e}')

    df = pd.DataFrame(all_rows, columns=['商店名稱', '品項', '菜單', '價格'])
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8-sig')
    print(f'共 {len(df)} 筆,已輸出至 {OUTPUT_CSV}')


if __name__ == '__main__':
    main()
