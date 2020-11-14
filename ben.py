from TikTokApi import TikTokApi
api = TikTokApi()
x = api.byUsername('therock', custom_verifyFp='verify_khgyofu6_YP8cEg4o_QpRA_4lbj_89kv_LOaIzzExQcAs', did='6894770323305154053', count=30)
# api.byUsername('therock', count=30)
# x = api.getUserObject('therock', custom_verifyFp='verify_khgyofu6_YP8cEg4o_QpRA_4lbj_89kv_LOaIzzExQcAs', did = '6894770323305154053', count=30)
print(x)

# url = 'https://m.tiktok.com/api/item_list/?aid=1988&app_name=tiktok_web&device_platform=web&referer=&user_agent=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F86.0.4240.198+Safari%2F537.36&cookie_enabled=true&screen_width=3440&screen_height=1440&browser_language=en-US&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F86.0.4240.198+Safari%2F537.36&browser_online=true&ac=4g&timezone_name=America%2FLos_Angeles&page_referer=https:%2F%2Fwww.tiktok.com%2F@benthamite&priority_region=&region=US&appType=m&isAndroid=false&isMobile=false&isIOS=false&OS=windows&count=30&id=6745191554350760966&secUid=MS4wLjABAAAAM3R2BtjzVT-uAtstkl2iugMzC6AtnpkojJbjiOdDDrdsTiTR75-8lyWJCY5VvDrZ&maxCursor=0&minCursor=0&sourceType=8&language=en'
# custom_verifyFp = 'verify_khgyofu6_YP8cEg4o_QpRA_4lbj_89kv_LOaIzzExQcAs'
# custom_did = '6894791469379962374'
# x = api.getData(url = url, custom_verifyFp = custom_verifyFp, custom_did = custom_did)
# print(x)