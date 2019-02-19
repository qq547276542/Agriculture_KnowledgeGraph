import hashlib
import time
import random
import string
from urllib.parse import quote
import base64
import requests
import os


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    return m.hexdigest().upper()


def get_params(image_base64):
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp = str(int(t))
     # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
     # 应用标志，这里修改成自己的id和key  
    app_id = '2112049951'
    app_key = 'Uv1JcL0n06McStku'
    params = {'app_id': app_id,
    'image': image_base64,
    'time_stamp': time_stamp,
    'nonce_str': nonce_str,
    'topk': '5',
    'format': '1'
    }
    sign_before = ''
    # 要对key排序再拼接  
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。  
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾  
    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名  
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params


def get_base64(src):
    with open(src, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s


def get_similar_entity(img_base64):
    # 去掉报头部分
    img_base64 = img_base64.split('base64,')[-1]
    url = 'https://api.ai.qq.com/fcgi-bin/vision/vision_objectr'
    payload = get_params(img_base64)
    try:
        r = requests.post(url, data=payload)
        print(r.json())
        ans = r.json()['data']['object_list']
        label_dict = {}
        with open(os.getcwd()+'/toolkit/id2obj.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                rows = line.split()
                for i, col in enumerate(rows):
                    if i % 2 == 0:
                        label_dict[int(rows[i])] = rows[i+1]
        for i in range(len(ans)):
            ans[i]['label_name'] = label_dict[ans[i]['label_id']]
    except Exception as e:
        print(e)
        ans = None
    return ans


if __name__ == '__main__':
    img_base64 = get_base64('/Users/chenyuanzhe/Downloads/yongdian.png')
    print(img_base64)
    print(get_similar_entity(img_base64))



# import base64
# from urllib import request, parse
#
#
# def get_base64(src):
#     with open(src, 'rb') as f:
#         base64_data = base64.b64encode(f.read())
#         s = base64_data.decode()
#         return s
#
# def get_similar_entity(img_base64):
#
#     # Base URL being accessed
#     url = 'https://api.ai.qq.com/fcgi-bin/vision/vision_objectr'
#
#     appkey = 'Uv1JcL0n06McStku'
#
#     # Dictionary of query parameters (if any)
#     parms = {
#         'app_id': '2112049951',
#         'image': img_base64,
#         'topk': 5,
#         'sign': ''
#     }
#
#     # Encode the query string
#     querystring = parse.urlencode(parms)
#
#     # Make a POST request and read the response
#     u = request.urlopen(url, querystring.encode('ascii'))
#     resp = u.read()

# from image_match.goldberg import ImageSignature
# import csv
# import pickle

# class Image_Matcher():
#     sig_dict = None
#     entity_list = []
#     label = {}
#     def __init__(self):
#         with open('image_ses.pkl', 'rb') as f:
#             self.sig_dict = pickle.load(f)
#         with open('../../predict_labels.txt', 'r', encoding='utf-8') as f:
#             for line in f.readlines():
#                 key = str(line.split()[0])
#                 value = int(line.split()[1])
#                 self.label[key] = value
#         with open("../../hudong_pedia.csv") as csvfile:
#             read = csv.reader(csvfile)
#             for i, row in enumerate(read):
#                 if i == 0:
#                     continue
#                 if int(self.label[row[0]]) in [5, 6, 9, 13] and row[0] in self.sig_dict:
#                     self.entity_list.append(row)
#
#         print('Image_Matcher init over!')
#
#     def get_similar_entity(self, url):
#         gis = ImageSignature()
#         cur_sig = gis.generate_signature(url)
#         ans = None
#         minn = 1.0
#         for row in self.entity_list:
#             dist = gis.normalized_distance(cur_sig, self.sig_dict[row[0]])
#             if dist < minn:
#                 minn = dist
#                 ans = row
#         if minn > 0.5:
#             return None
#         return ans


# a = Image_Matcher()
# url = 'https://gss2.bdstatic.com/9fo3dSag_xI4khGkpoWK1HF6hhy/baike/s%3D220/sign=63e0b443564e9258a23481ecac83d1d1/8694a4c27d1ed21b643772c2ad6eddc451da3f1e.jpg'
# print(a.get_similar_entity(url))