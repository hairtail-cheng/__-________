from lxml import etree
from wordcloud import WordCloud
import requests
import re


header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
			              'Chrome/43.0.2357.130 Safari/537.36',
			'Referer': 'https://www.bilibili.com/v/douga?spm_id_from=333.334.b_62696c695f646f756761.2'
		}
bv = 'BV1wE411t7Mz'
url = 'https://www.bilibili.com/video/' + bv

html = requests.get(url, headers=header)
html.encoding = html.apparent_encoding

# 通过正则表达式查找得到可以指向弹幕网页的链接cid
match = r'cid=(.*)&aid'
cid = re.search(match, html.text).group().replace('cid=', '').replace('&aid', '')

comment_url = 'https://comment.bilibili.com/' + str(cid) + '.xml'
comment_text = requests.get(comment_url, headers=header)
comment_selector = etree.HTML(comment_text.content)
comment_content = comment_selector.xpath('//i')
a = []
for comment_each in comment_content:
	comments = comment_each.xpath('//d/text()')
	if comments:
		for comment in comments:
			a.append(comment)


wc = WordCloud(font_path='../static/simkai.ttf', background_color='White', max_words=2000, max_font_size=40)

wc.generate(','.join(a))
wc.to_file('5.png')

