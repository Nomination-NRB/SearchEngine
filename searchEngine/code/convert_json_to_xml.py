# -*- coding: utf-8 -*-
import json
import re
from xml.etree.ElementTree import Element, SubElement, tostring

json_data = '{"news_id": "470308283", "keywords": "借鉴：这篇最受欢迎校训，没有一个字讲学习", "desc": ' \
            '"“我知道来的；我是为了通过各种苦乐逆顺的体验来历练自己而来的，并由此", "title": "借鉴：这篇最受欢迎校训，没有一个字讲学习", "source": "龙乡教育", "time": "10-14 ' \
            '21:55", "content": "关注123456789"} '

data = json.loads(json_data)

root = Element('doc')

SubElement(root, 'id').text = data['news_id']
SubElement(root, 'url').text = 'http://www.baidu.com'
SubElement(root, 'source').text = data['source']
SubElement(root, 'title').text = data['title']
SubElement(root, 'datetime').text = data['time']
SubElement(root, 'body').text = data['content']

xml_string = tostring(root, encoding='utf-8', xml_declaration=True).decode()

print(xml_string)

i = 1
with open('填入你的json文件路径', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        root = Element('doc')
        SubElement(root, 'id').text = str(i)
        SubElement(root, 'url').text = 'http://www.baidu.com'
        SubElement(root, 'source').text = data['source']
        SubElement(root, 'title').text = data['title']
        SubElement(root, 'datetime').text = '2022-' + data['time'] + ':00'
        SubElement(root, 'body').text = data['content']
        xml_string = tostring(root, encoding='utf-8', xml_declaration=True).decode()
        news_id = data['news_id']

        if not (re.search('[\u4e00-\u9fa5]', data['title'])):
            continue
        if not (re.search('[\u4e00-\u9fa5]', data['content'])):
            continue

        with open(f'/searchEngine/data/new_xml/{i}.xml', 'w', encoding='utf-8') as out_file:
            out_file.write(xml_string)
        i = i + 1
        # 只保存5000条
        if i == 5001:
            break
