import requests


def webpackCompilationHash():
    headers = {
        'Referer': 'https://www.deepl.com/',
        'Origin': 'https://www.deepl.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get('https://static.deepl.com/gatsby/page-data/app-data.4c7d8001.json', headers=headers)
    print(response.json())


webpackCompilationHash()
webpackCompilationHash()
webpackCompilationHash()
