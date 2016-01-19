# coding=UTF-8
import requests
from bs4 import BeautifulSoup

URL_ROOT = "http://jirs.judicial.gov.tw/FJUD/"
URL_HOME = "http://jirs.judicial.gov.tw/FJUD/FJUDQRY01_1.aspx"
URL_SEARCH = "http://jirs.judicial.gov.tw/FJUD/FJUDQRY02_1.aspx"
DATA = {
    'v_court': "TPD 臺灣臺北地方法院",
    'v_sys': "V",
    'jud_year': "",
    'sel_judword': "常用字別",
    'jud_case': "",
    'jud_no': "",
    'jud_no_end': "",
    'jt': "",
    'dy1': "95",
    'dm1': "1",
    'dd1': "1",
    'dy2': "98",
    'dm2': "9",
    'dd2': "21",
    'jmain1': "",
    'kw': "業務過失",
    'keyword': "業務過失",
    'sdate': "20060101",
    'edate': "20090921",
    'jud_title': "",
    'jmain': "",
    'Button': " 查詢",
    'searchkw': "過失"
}

headers = {
    "Host": " jirs.judicial.gov.tw",
    "Connection": " keep-alive",
    "Content-Length": " 438",
    "Cache-Control": " max-age=0",
    "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Origin": " http://jirs.judicial.gov.tw",
    "Upgrade-Insecure-Requests": " 1",
    "User-Agent": " Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Content-Type": " application/x-www-form-urlencoded",
    "DNT": " 1",
    "Referer": " http://jirs.judicial.gov.tw/FJUD/FJUDQRY01_1.aspx",
    "Accept-Encoding": " gzip, deflate",
    "Accept-Language": " zh-TW,zh;q=0.8,ja;q=0.6,en;q=0.4"
}

request = requests.Session()

content = request.post(URL_SEARCH, data=DATA, headers=headers).content

dom = BeautifulSoup(content, "html.parser")

try:
    for row in dom.find('table', id='Table3').find_all('tr'):
        fields = row.find_all('td')
        if len(fields) > 0:
            entity = {
                'SN': fields[0].text,
                'judgment_number': fields[1].text,
                'judgement_link': fields[1].find('a')['href'],
                'date': fields[2].text,
                'summary': fields[3].text
            }

            judgement_link_headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-TW,zh;q=0.8,ja;q=0.6,en;q=0.4",
                "Connection": "keep-alive",
                "DNT": "1",
                "Host": "jirs.judicial.gov.tw",
                "Referer": "http://jirs.judicial.gov.tw/FJUD/FJUDQRY02_1.aspx",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            }
            dom_judgement_link = BeautifulSoup(request.post(URL_ROOT+entity['judgement_link'], data=DATA, headers=judgement_link_headers).content, 'html.parser')
            entity['judgement_content'] = dom_judgement_link.find('pre').text

except Exception, e:
    print '===============html content===============\n', content
    print '===============DOM===============\n', dom
    print '===============error===============\n', e
