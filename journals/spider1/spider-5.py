# 网址首页：https://www.sciencedirect.com/journal/american-journal-of-kidney-diseases/issues
# 网址入口：https://www.sciencedirect.com/journal/02726386/year/2018/issues
# 期刊列表：https://www.sciencedirect.com/journal/kidney-international-supplements/vol/24/issue/6
# 文章详情：https://www.sciencedirect.com/science/article/abs/pii/S193131281830595X
# 只检测一个
import requests
from lxml import etree
from fake_useragent import UserAgent
import re
import json
import time
import queue
import pymysql
import threading
import random

start = time.time()
count = 0
class ArticleSpider:
    def __init__(self):
        self.headers = UserAgent().random
        self.conn = None

    def writeFile(self, file, content):
        with open(file, 'a', encoding='utf-8') as fw:
            fw.write(content)

    def readFile(self, file):
        with open(file, 'r', encoding='utf-8') as fr:
            return fr.read()

    def get_reponse(self, url, params='', headers=''):
        if headers == '':
            headers = {
                "User-Agent": self.headers,
            }
        i = 1  # 循环次数
        while True:
            try:
                s = requests.session()
                s.keep_alive = 'false'
                res = s.get(url, params=params, headers=headers,
                            timeout=150)
                if res.status_code == 200:
                    # 向数据队列里追加,以元组形式追加，用以解析出错保存url
                    result = res.text
                    return result
                else:
                    print(res.status_code)
            except Exception as e:
                print('请求错误：', e)
            if i > 3:
                return ''
            else:
                time.sleep(random.random() * 5)
                print(f'请求出错，正在进行第{i}次重试...')
                i += 1

    def get_conn(self):
        """获取数据的链接"""
        if not self.conn:
            self.conn = pymysql.connect(host='localhost', user='root', password='root', database='article', port=3306)
        return self.conn

    def get_first(self, q):
        while True:
            # 获取年份
            lock.acquire()
            try:
                if q.qsize() > 0:
                    years = q.get()
                    print(f'正在爬取第{years}年')
                else:
                    break
            finally:
                pass
                lock.release()
            first_count = 0  # 重试次数
            while True:
                # https://www.sciencedirect.com/journal/02726386/year/2018/issues
                url = 'https://www.sciencedirect.com/journal/02726386/year/{0}/issues'.format(str(years))
                # print('年份url：',url)
                try:
                    headers = {
                        'authority': 'www.sciencedirect.com',
                        'accept-language': 'zh-CN,zh;q=0.9',
                        'cookie': '__cfduid=d411520331022b2bd67c831fe272e67561568698645; EUID=2b03e1b6-db08-49bb-ad43-240580ec97b7; __gads=ID=9e1ffa56084ba736:T=1568698655:S=ALNI_MYF4S3DzhutyFh94Zmtrj8HD0CrVw; utt=d043-95383b9ad6122c5ee52e9d22306a4ae60c2-cr5W; sd_session_id=5163345b37fb4849b719bb874f3d3b430289gxrqa; ANONRA_COOKIE=3255091529086FFD994EB05D3915612F286F30ED2051B7B3C6301C849BF56E590309157B8342825BC1BB72F2592506B2616F48B461E47324; fingerPrintToken=f12d3695d2f9350d7c1c7f7306e23300; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; acw=5163345b37fb4849b719bb874f3d3b430289gxrqa%7C%24%7C441DBA04D428FBF98A0B44222F84F9148AD896EE7FA4A5379C41986730244BE636FCEE43428438D246C0B525EF9A291267FCF61C27EECDC03FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; mbox=session%23bfca2d0d8d154ce89fc5fbe1d2da9166%231573187104%7CPC%23111570512652041-937310.21_26%231636430044; SD_ART_LINK_STATE=%3Ce%3E%3Cq%3Escience%3C%2Fq%3E%3Corg%3Ejrnl_issue%3C%2Forg%3E%3Cz%3Erslt_list_item%3C%2Fz%3E%3Crdt%3E2019%2F11%2F08%2F03%3A54%3A35%3A389%3C%2Frdt%3E%3Cenc%3EN%3C%2Fenc%3E%3C%2Fe%3E; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-1712354808%7CMCIDTS%7C18208%7CMCMID%7C59211882685600195233779018425128822394%7CMCAAMLH-1573794957%7C11%7CMCAAMB-1573794957%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1573197357s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1136952377%7CvVersion%7C4.3.0; MIAMISESSION=6a0656ba-ccbc-47cb-9148-8d630c46030a:3750643136; RT="z=1&dm=sciencedirect.com&si=6e5bb40c-75b9-4dfa-8353-2ea33db1559a&ss=k2plw7bo&sl=1&tt=qe&bcn=%2F%2F60062f05.akstat.io%2F&ld=30i71"; s_pers=%20c19%3Dsd%253Abrowse%253Ajournal%253Aarchive%7C1573192137172%3B%20v68%3D1573190337018%7C1573192137185%3B%20v8%3D1573190375771%7C1667798375771%3B%20v8_s%3DLess%2520than%25201%2520day%7C1573192175771%3B; s_sess=%20s_cpc%3D0%3B%20s_ppvl%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C13%252C13%252C180%252C1366%252C180%252C1366%252C768%252C1%252CP%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dsd%25253Abrowse%25253Ajournal%25253Aarchive%252C57%252C6%252C1662%252C1366%252C362%252C1366%252C768%252C1%252CP%3B%20s_sq%3Delsevier-sd-prod%25252Celsevier-global-prod%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dsd%2525253Abrowse%2525253Ajournal%2525253Aarchive%252526link%25253D2018%25252520%252525E2%25252580%25252594%25252520Volumes%2525252071-72%252526region%25253Daa-issues-archive%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%252526pid%25253Dsd%2525253Abrowse%2525253Ajournal%2525253Aarchive%252526pidt%25253D1%252526oid%25253Dfunctiontc%25252528%25252529%2525257B%2525257D%252526oidt%25253D2%252526ot%25253DBUTTON%3B',
                        'scheme': 'https',
                        #referer需要换！！！
                        'referer': 'https://www.sciencedirect.com/journal/american-journal-of-kidney-diseases/issues',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'same-origin',
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                    }
                    content = requests.get(url=url, headers=headers, timeout=200).text
                    root = re.compile('"uriLookup":"(.*?)"', re.S)
                    first_list = root.findall(content)
                    if first_count == 3:
                        self.writeFile('first_error5.log', url + '\n')
                        break
                    elif len(first_list) == 0:
                        # 如果没有获取到信息就重新请求
                        first_count += 1
                        continue
                    else:
                        for i in first_list:
                            # https://www.sciencedirect.com/journal/american-journal-of-kidney-diseases/vol/72/issue/6
                            second_link = 'https://www.sciencedirect.com/journal/american-journal-of-kidney-diseases{0}'.format(
                                str(i))
                            # print('i', second_link)
                            self.get_second(second_link)
                        break
                except Exception as e:
                    print('first_error:', e)
                    self.writeFile('first_error5.log', url + '\n')

                time.sleep(2)

    # 将二级页面内容存入队列
    def get_second(self, second_url):
        second_count = 0  # 重试次数
        article_list = []
        url = second_url
        # print('得到二级链接：', url)
        while True:
            try:
                headers = {
                    'authority': "www.sciencedirect.com",
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'async': 'false',
                    'scheme': 'https',
                    'cookie': '__cfduid=d411520331022b2bd67c831fe272e67561568698645; EUID=2b03e1b6-db08-49bb-ad43-240580ec97b7; __gads=ID=9e1ffa56084ba736:T=1568698655:S=ALNI_MYF4S3DzhutyFh94Zmtrj8HD0CrVw; utt=d043-95383b9ad6122c5ee52e9d22306a4ae60c2-cr5W; sd_session_id=5163345b37fb4849b719bb874f3d3b430289gxrqa; ANONRA_COOKIE=3255091529086FFD994EB05D3915612F286F30ED2051B7B3C6301C849BF56E590309157B8342825BC1BB72F2592506B2616F48B461E47324; fingerPrintToken=f12d3695d2f9350d7c1c7f7306e23300; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; acw=5163345b37fb4849b719bb874f3d3b430289gxrqa%7C%24%7C441DBA04D428FBF98A0B44222F84F9148AD896EE7FA4A5379C41986730244BE636FCEE43428438D246C0B525EF9A291267FCF61C27EECDC03FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; mbox=session%23bfca2d0d8d154ce89fc5fbe1d2da9166%231573187104%7CPC%23111570512652041-937310.21_26%231636430044; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-1712354808%7CMCIDTS%7C18208%7CMCMID%7C59211882685600195233779018425128822394%7CMCAAMLH-1573794957%7C11%7CMCAAMB-1573794957%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1573197357s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1136952377%7CvVersion%7C4.3.0; MIAMISESSION=6a0656ba-ccbc-47cb-9148-8d630c46030a:3750643136; s_pers=%20c19%3Dsd%253Abrowse%253Ajournal%253Aarchive%7C1573192137172%3B%20v68%3D1573190337018%7C1573192137185%3B%20v8%3D1573190403433%7C1667798403433%3B%20v8_s%3DLess%2520than%25201%2520day%7C1573192203433%3B; s_sess=%20s_cpc%3D0%3B%20s_ppvl%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C13%252C13%252C180%252C1366%252C180%252C1366%252C768%252C1%252CP%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dsd%25253Abrowse%25253Ajournal%25253Aarchive%252C57%252C6%252C1662%252C1366%252C150%252C1366%252C768%252C1%252CP%3B%20s_sq%3Delsevier-sd-prod%25252Celsevier-global-prod%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dsd%2525253Abrowse%2525253Ajournal%2525253Aarchive%252526link%25253Dissue%25252520title%252526region%25253Daa-issues-archive%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%252526pid%25253Dsd%2525253Abrowse%2525253Ajournal%2525253Aarchive%252526pidt%25253D1%252526oid%25253Dhttps%2525253A%2525252F%2525252Fwww.sciencedirect.com%2525252Fjournal%2525252Famerican-journal-of-kidney-diseases%2525252Fvol%2525252F73%2525252Fissue%2525252F1%252526ot%25253DA%3B; SD_ART_LINK_STATE=%3Ce%3E%3Cq%3Escience%3C%2Fq%3E%3Corg%3Ejrnl_archive%3C%2Forg%3E%3Cz%3Erslt_list_item%3C%2Fz%3E%3Crdt%3E2019%2F11%2F08%2F05%3A20%3A03%3A447%3C%2Frdt%3E%3Cenc%3EN%3C%2Fenc%3E%3C%2Fe%3E; RT="z=1&dm=sciencedirect.com&si=6e5bb40c-75b9-4dfa-8353-2ea33db1559a&ss=k2pownwo&sl=0&tt=0&bcn=%2F%2F684fc537.akstat.io%2F&ld=30i71&nu=8ed69f04e60432ba279b8d8848d0dc2c&cl=1fg0&ul=1g8l"',
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                }
                second_html = requests.get(url=url, headers=headers, timeout=150).text
                root = etree.HTML(second_html)
                second_list = root.xpath(
                    '//a[@class="anchor article-content-title u-margin-xs-top u-margin-s-bottom"]/@href')
                second_id = root.xpath(
                    '//a[@class="anchor article-content-title u-margin-xs-top u-margin-s-bottom"]/@id')

                if second_count == 3:
                    self.writeFile('second_error5.log', url + '\n')
                    break
                elif len(second_list) == 0:
                    # 如果没有获取到信息就重新请求
                    second_count += 1
                    continue
                else:
                    for i, j in zip(second_list, second_id):
                        # https://www.sciencedirect.com/science/article/pii/S1074552115004482
                        three_url = "https://www.sciencedirect.com{0}".format(str(i))
                        # print('three_url', three_url)
                        self.get_three(three_url, j, url)
                    break
            except Exception as e:
                print('second_error:', e)
                self.writeFile('second_error5.log', url + '\n')
            time.sleep(2)

    # 将三级页面内容存入队列
    def get_three(self, second_url, second_id, url):
        # time.sleep(0.5)
        article_url = second_url
        while True:
            try:
                headers = {
                    'authority': "www.sciencedirect.com",
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'async': 'false',
                    'scheme': 'https',
                    'cookie': '__cfduid=d411520331022b2bd67c831fe272e67561568698645; EUID=2b03e1b6-db08-49bb-ad43-240580ec97b7; __gads=ID=9e1ffa56084ba736:T=1568698655:S=ALNI_MYF4S3DzhutyFh94Zmtrj8HD0CrVw; utt=d043-95383b9ad6122c5ee52e9d22306a4ae60c2-cr5W; sd_session_id=5163345b37fb4849b719bb874f3d3b430289gxrqa; ANONRA_COOKIE=3255091529086FFD994EB05D3915612F286F30ED2051B7B3C6301C849BF56E590309157B8342825BC1BB72F2592506B2616F48B461E47324; fingerPrintToken=f12d3695d2f9350d7c1c7f7306e23300; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; acw=5163345b37fb4849b719bb874f3d3b430289gxrqa%7C%24%7C441DBA04D428FBF98A0B44222F84F9148AD896EE7FA4A5379C41986730244BE636FCEE43428438D246C0B525EF9A291267FCF61C27EECDC03FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-1712354808%7CMCIDTS%7C18208%7CMCMID%7C59211882685600195233779018425128822394%7CMCAAMLH-1573794957%7C11%7CMCAAMB-1573794957%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1573197357s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1136952377%7CvVersion%7C4.3.0; MIAMISESSION=6a0656ba-ccbc-47cb-9148-8d630c46030a:3750643203; mbox=session%23093c6f507ec24610b05d9d4f2bf056c3%231573192265%7CPC%23111570512652041-937310.21_26%231636435205; s_pers=%20c19%3Dsd%253Abrowse%253Ajournal%253Aissue%7C1573192209855%3B%20v68%3D1573190409688%7C1573192209871%3B%20v8%3D1573190447645%7C1667798447645%3B%20v8_s%3DLess%2520than%25201%2520day%7C1573192247645%3B; s_sess=%20s_cpc%3D0%3B%20s_ppvl%3Dsd%25253Abrowse%25253Ajournal%25253Aarchive%252C57%252C6%252C1662%252C1366%252C150%252C1366%252C768%252C1%252CP%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dsd%25253Abrowse%25253Ajournal%25253Aissue%252C19%252C2%252C1232%252C1366%252C332%252C1366%252C768%252C1%252CP%3B%20s_sq%3Delsevier-sd-prod%25252Celsevier-global-prod%253D%252526c.%252526a.%252526activitymap.%252526page%25253Dsd%2525253Abrowse%2525253Ajournal%2525253Aissue%252526link%25253DKidney%25252520Function%25252520and%25252520Hospital-Acquired%25252520Infections%2525253A%25252520Worth%25252520a%25252520Deeper%25252520Look%252526region%25253Darticle-list%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%252526pid%25253Dsd%2525253Abrowse%2525253Ajournal%2525253Aissue%252526pidt%25253D1%252526oid%25253Dhttps%2525253A%2525252F%2525252Fwww.sciencedirect.com%2525252Fscience%2525252Farticle%2525252Fpii%2525252FS0272638618310138%252526ot%25253DA%3B; SD_ART_LINK_STATE=%3Ce%3E%3Cq%3Escience%3C%2Fq%3E%3Corg%3Ejrnl_issue%3C%2Forg%3E%3Cz%3Erslt_list_item%3C%2Fz%3E%3Crdt%3E2019%2F11%2F08%2F05%3A20%3A47%3A664%3C%2Frdt%3E%3Cenc%3EN%3C%2Fenc%3E%3C%2Fe%3E; RT="z=1&dm=sciencedirect.com&si=6e5bb40c-75b9-4dfa-8353-2ea33db1559a&ss=k2pownwo&sl=1&tt=4bf&bcn=%2F%2F684fc537.akstat.io%2F&ld=1lty&nu=e3638fb2801954ed7f7d6b9617046bed&cl=2ebw&ul=2ecs"',
                    'referer': str(url),
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
                }
                reg = re.compile('"entitledToken":"(.*?)"', re.S)
                response = requests.get(url=article_url, headers=headers, timeout=150).text
                if reg.findall(response):
                    entitledToken = reg.findall(response)[0]
                    reg = re.compile('<a class="doi".*?"(.*?)" ', re.S)
                    DOI = reg.findall(response)[0]
                    # 文章json数据的链接
                    new_url = 'https://www.sciencedirect.com/sdfe/arp/pii/{0}/body?entitledToken={1}'.format(
                        str(second_id), str(entitledToken))
                    # 文章底部的Reference的引用数据（Json数据）的URL！！！
                    new_link = 'https://www.sciencedirect.com/sdfe/arp/pii/{0}/references?entitledToken={1}'.format(
                        str(second_id), str(entitledToken))
                    article_html = requests.get(url=new_url, headers=headers, timeout=(150, 200)).text
                    referce_html = requests.get(url=new_link, headers=headers, timeout=(150, 200)).text
                    time.sleep(0.25)

                    if len(article_html) != 0:
                        if json.loads(referce_html)['content'] != []:
                            article_json = json.loads(article_html)
                            referce_json = json.loads(referce_html)
                            # print('doi:',DOI)
                            reg1 = re.compile('"_":"(.*?)"}', re.S | re.M)
                            data = reg1.findall(response)
                            Abstract_text = ''
                            if data[0] in ['Abstract', 'Background', 'Summary']:
                                for i in data[1:-1]:
                                    Abstract_text = Abstract_text + ' ' + str(i.strip())
                                Abstract_text = data[0] + Abstract_text
                            self.get_article(article_url, second_id, DOI, article_json, referce_json, Abstract_text)
                            break
                        else:
                            # print('只有文献')
                            self.writeFile('OnlyReferences5.log', article_url + '\n')
                            break
                    else:
                        # print('没有文章')
                        self.writeFile('NullArticle5.log', article_url + '\n')
                        break
                else:
                    break
            except Exception as e:
                print('three_error:', article_url, e)
                self.writeFile('ErrorArticle5.log', article_url + '\n')
            time.sleep(3)

    def get_article(self, article_url, second_id, DOI, article_json, referce_json, Abstract_text):

        conn = self.get_conn()
        # 获取游标，然后插入数据
        cursor = conn.cursor()
        global count
        article_count = 0
        while True:
            try:
                image = article_json['attachments']
                # 图片说明
                image_text = article_json['floats']
                n = len(image_text)  # 图片列表长度
                # 文章数据
                article_data = article_json['content']
                # 文献数据
                references = referce_json['content']
                lock.acquire()
                # 插入数据库/把一篇文章的所有图片插入数据，如果有失败的就整篇文章留下下次操作
                # 判断文章是否存在，如果存在直接跳过，中间出错回滚
                # 检测文章是否存在
                existence = cursor.execute('select DOI from papers_l where DOI=(%s)', args=(DOI,))
                if existence:
                    print('文章已存在')
                    pass
                else:
                    article_list = []
                    for text1, i, j in zip(image_text, range(0, n), image):
                        img_text = text1['$$']
                        reg = re.compile("'_':(.*?)}", re.S)
                        data = reg.findall(str(img_text))
                        re1 = re.compile("'locator':(.*?),", re.S)
                        data2 = re1.findall(str(text1))
                        img_list = []
                        if data2 != []:
                            if len(data2[0]) == 6:
                                data3 = data2[0]
                            else:
                                d = data2[0][2:5]
                                data3 = str(d)
                            img_url = 'https://ars.els-cdn.com/content/image/1-s2.0-' + str(
                                second_id) + '-' + str(data3) + '.jpg'
                        else:
                            img_url = " "
                        article_text = ""
                        for i in data:
                            article_text = article_text + str(eval(i.strip()))
                            FigureDescription = str(eval(data[0])) + "." + str(
                                eval(data[1])) + " " + article_text
                            title = eval(data[0])
                            if len(FigureDescription) == 0:
                                print('没有图片描述')
                                break
                        item = (DOI, img_url, title, FigureDescription, url)
                        img_list.append(item)
                        # 保存图片
                        cursor.executemany('insert into figures_l values(%s,%s,%s,%s,%s)',
                                           args=img_list)
                    time.sleep(1)
                    for contents, reference in zip(article_data, references):
                        content = contents['$$']
                        reference = reference['$$']
                        reg = re.compile("'_':(.*?)}", re.S)
                        data = reg.findall(str(content))
                        list1 = []

                        for i in data:
                            list1.append((i.strip()).replace("'", ''))
                        article_text = ' '.join(list1)
                        data = re.findall("'_': '(.*?)'}", str(reference), re.S | re.M)
                        ref_list = []
                        for j in data:
                            ref_list.append((j.strip()).replace("'", ''))
                        reference_text = ' '.join(ref_list)

                        Content = Abstract_text + " " + article_text + " " + reference_text
                        item = (0, DOI, Content)
                        article_list.append(item)
                        # 插入文章
                        cursor.executemany('insert into papers_l values(%s,%s,%s)', args=article_list)
                        # 一篇文章入库后结束事务
                        conn.commit()
                        print('文章已入库')
                        count += 1
                        print(f'第{count}篇文章已爬取')
                        time.sleep(1.5)
                break
            except Exception as e:
                print('article_error:', e)
                self.writeFile('article_error5.log', article_url + '\n')
                # 如果插入失败就进行回滚操作
                conn.rollback()
                break
            time.sleep(5)
        lock.release()

if __name__ == '__main__':
    lock = threading.Lock()
    q = queue.Queue(maxsize=20)

    # 网站首页
    url = 'https://www.sciencedirect.com/journal/american-journal-of-kidney-diseases/issues'
    headers = {
        'authority': 'www.sciencedirect.com',
        # 'Connection': 'close',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '__cfduid=d411520331022b2bd67c831fe272e67561568698645; EUID=2b03e1b6-db08-49bb-ad43-240580ec97b7; __gads=ID=9e1ffa56084ba736:T=1568698655:S=ALNI_MYF4S3DzhutyFh94Zmtrj8HD0CrVw; utt=d043-95383b9ad6122c5ee52e9d22306a4ae60c2-cr5W; sd_session_id=5163345b37fb4849b719bb874f3d3b430289gxrqa; ANONRA_COOKIE=3255091529086FFD994EB05D3915612F286F30ED2051B7B3C6301C849BF56E590309157B8342825BC1BB72F2592506B2616F48B461E47324; fingerPrintToken=f12d3695d2f9350d7c1c7f7306e23300; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; acw=5163345b37fb4849b719bb874f3d3b430289gxrqa%7C%24%7C441DBA04D428FBF98A0B44222F84F9148AD896EE7FA4A5379C41986730244BE636FCEE43428438D246C0B525EF9A291267FCF61C27EECDC03FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; mbox=session%23bfca2d0d8d154ce89fc5fbe1d2da9166%231573187104%7CPC%23111570512652041-937310.21_26%231636430044; SD_ART_LINK_STATE=%3Ce%3E%3Cq%3Escience%3C%2Fq%3E%3Corg%3Ejrnl_issue%3C%2Forg%3E%3Cz%3Erslt_list_item%3C%2Fz%3E%3Crdt%3E2019%2F11%2F08%2F03%3A54%3A35%3A389%3C%2Frdt%3E%3Cenc%3EN%3C%2Fenc%3E%3C%2Fe%3E; MIAMISESSION=6a0656ba-ccbc-47cb-9148-8d630c46030a:3750642954; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-1712354808%7CMCIDTS%7C18208%7CMCMID%7C59211882685600195233779018425128822394%7CMCAAMLH-1573794957%7C11%7CMCAAMB-1573794957%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1573197357s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1136952377%7CvVersion%7C4.3.0; s_pers=%20c19%3Dsd%253Aproduct%253Ajournal%253Aarticle%7C1573191957651%3B%20v68%3D1573190154585%7C1573191957659%3B%20v8%3D1573190157690%7C1667798157690%3B%20v8_s%3DLess%2520than%25201%2520day%7C1573191957690%3B; s_sess=%20s_cpc%3D0%3B%20s_sq%3D%3B%20s_ppvl%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C20%252C20%252C236%252C1106%252C236%252C1366%252C768%252C1%252CP%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C13%252C13%252C180%252C1366%252C180%252C1366%252C768%252C1%252CP%3B; RT="z=1&dm=sciencedirect.com&si=6e5bb40c-75b9-4dfa-8353-2ea33db1559a&ss=k2plw7bo&sl=0&tt=0&bcn=%2F%2F60062f05.akstat.io%2F&ul=30ghm"',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    }
    response = requests.get(url=url, headers=headers, timeout=120).text
    data = etree.HTML(response)
    # 年份列表
    years = data.xpath('//span[@class="accordion-title js-accordion-title"]/text()')
    # 翻页
    # next_link = data.xpath('//link[@rel="next"]/@href')
    for year in years:
        r = year[0:4]
        q.put(r)
    # 期刊列表的第一页2019-2003
    # 线程锁
    lock = threading.Lock()
    # # 线程池用来存放线程
    pool = []
    # # 开启5个线程
    for x in range(20):
        article = ArticleSpider()
        th = threading.Thread(target=article.get_first, args=(q,))
        pool.append(th)
        th.start()
    for th in pool:
        th.join()
    print('ok')
    end = time.time()
    print('花费时间：', start - end)
