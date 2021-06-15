import requests


def spider_baidu(page=1, num=4, keyword='美女'):
    if page == 0:
        page = 1
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    pn = ((page - 1) * num) + 1
    img_path_list = []
    # pn是从第几张图片获取 百度图片下滑时默认一次性显示30张

    url = 'https://image.baidu.com/search/acjson?'
    param = {
        'tn': 'resultjson_com',
        'logid': '8846269338939606587',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': keyword,
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '-1',
        'z': '',
        'ic': '',
        'hd': '',
        'latest': '',
        'copyright': '',
        'word': keyword,
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '0',
        'istype': '2',
        'qc': '',
        'nc': '1',
        'fr': '',
        'expermode': '',
        'force': '',
        'cg': '',
        'pn': pn,  # 从第几张图片开始
        'rn': num,
        'gsm': '1e',
    }
    page_text = requests.get(url=url, headers=header, params=param)
    page_text.encoding = 'utf-8'
    page_text = page_text.json()
    info_list = page_text['data']
    del info_list[-1]
    for i in info_list:
        img_path_list.append(i['thumbURL'])
    return img_path_list


if __name__ == '__main__':
    url = spider_baidu(page=2, num=4, keyword='风景')
    print(url)
