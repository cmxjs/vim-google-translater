# -*- coding: utf-8 -*-
import sys
import io
import platform
import re
import ssl
from urllib import parse
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
ssl._create_default_https_context = ssl._create_unverified_context


class Translate_API():
    def __init__(self):
        self.host = 'translate.google.cn'

    def headers(self):
        headers = {
            'Host': self.host,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'Referer': 'https://' + self.host,
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
        return headers

    def get_Tkk(self):
        url = 'https://' + self.host
        try:
            req = Request(url=url, headers=self.headers())
            resp = urlopen(req).read()
            string = resp.decode()
            self.Tkk = re.search(r'tkk\:\'(\d+\.\d+)?\'', string).group(1)
        except Exception as e:
            print(e)
            return True
        else:
            return False

    def get_Token(self, string):
        def ch2ascii():
            asciis = []
            f = 0
            for ch in string:
                asc = ord(ch)
                if asc < 128:
                    asciis.append(asc)
                else:
                    if asc < 2048:
                        asciis.append((asc >> 6) | 192)
                    else:
                        if (55296 == (asc & 64512)) and (f + 1 < len(string)) and (
                                56320 == (ord(string[f+1]) & 64512)):
                            f += 1
                            asc = 65536 + ((asc & 1023) << 10) + \
                                (ord(string[f]) & 1023)
                            asciis.append((asc >> 18) | 240)
                            asciis.append((asc >> 12) & 63 | 128)
                        else:
                            asciis.append((asc >> 12) | 224)
                            asciis.append((asc >> 6) & 63 | 128)
                    asciis.append((asc & 63) | 128)
                f += 1
            else:
                return asciis

        def RL(a, b):
            for d in range(0, len(b)-2, 3):
                c = b[d + 2]
                c = ord(c[0]) - 87 if 'a' <= c else int(c)
                c = a >> c if '+' == b[d + 1] else a << c
                a = a + c & 4294967295 if '+' == b[d] else a ^ c
            return a

        if self.get_Tkk():
            return True

        asciis = ch2ascii()
        e = self.Tkk.split('.')
        h = int(e[0]) or 0
        t = h
        for item in asciis:
            t += item
            t = RL(t, '+-a^+6')
        t = RL(t, '+-3^+b+-f')
        t ^= int(e[1]) or 0
        if 0 > t:
            t = (t & 2147483647) + 2147483648
        result = t % 1000000
        self.ToKen = str(result) + '.' + str(result ^ h)
        return False

    def translate(self, query, tl, sl='auto'):
        # tl = (zh-CH en)
        params = {
            'client': 'webapp',
            'sl': sl,
            'tl': tl,
            'v': '1.0',
            'source': 'is',
        }
        url = 'https://' + self.host + '/translate_a/t?'
        if self.get_Token(query):
            return True
        params['tk'] = self.ToKen
        params['q'] = query
        try:
            url_data = parse.urlencode(params)
            req = Request(url=url+url_data, headers=self.headers())
            resp = urlopen(req).read().decode()
            string = re.search('^\[\"(.+)\"\]', resp).group(1)
        except Exception as e:
            print(e)
            return True
        else:
            self.result = string
            return False


def contain_chinese(check_str):
    for ch in check_str:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def str_decode(word):
    if sys.version_info >= (3, 0):
        return word
    else:
        return word.decode('utf-8')


def get_word_info(string):
    translate_obj = Translate_API()
    translate_obj.get_Token(string)
    tl = 'en' if contain_chinese(string) else 'zh-CH'
    translate_obj.translate(query=string, tl=tl)
    return translate_obj.result


if __name__ == "__main__":
    if(platform.system() == 'Windows'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
    argv = sys.argv
    try:
        info = get_word_info(str_decode("".join(argv[1:])))
    except Exception as e:
        info = "翻译失败:{}".format(e)
    finally:
        sys.stdout.write(info)
