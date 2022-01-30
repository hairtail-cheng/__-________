import datetime
from io import BytesIO

import jieba
from django.shortcuts import render
import requests
from user.models import *
import json
import re
from lxml import etree
from wordcloud import WordCloud
import warnings

warnings.filterwarnings("ignore")


class spyder:
	def __init__(self, detail):
		self.detail = detail
		self.header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
			              'Chrome/43.0.2357.130 Safari/537.36',
			'Referer': 'https://www.bilibili.com/v/douga?spm_id_from=333.334.b_62696c695f646f756761.2'
		}

	def up_detail(self, mid):
		try:
			url = 'https://api.bilibili.com/x/web-interface/card?mid=' + mid
			http = requests.get(url, headers=self.header)
			data = json.loads(http.text)
			if data['data']['card']:
				result = {
					'result': '200',
					'data': {
						'name': data['data']['card']['name'],
						'face': data['data']['card']['face'],
						'fans': str(data['data']['card']['fans']),
						'sign': data['data']['card']['sign'].strip()
					}
				}
				return result
			else:
				return {'result': '没有找到该up'}
		except:
			return {'result': '没有找到该up'}

	def all_video(self, mid):
		import math
		url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}'
		fa = json.loads(requests.get(url, headers=self.header).text)
		count = fa['data']['page']['count']

		data1 = fa['data']['list']['vlist']
		pages = math.ceil(count / 30)

		for i in range(2, pages + 1):
			data1 += json.loads(requests.get(url + f"&pn={str(i)}", headers=self.header).text)['data']['list']['vlist']

		data = []

		for i in data1:
			vd = {
				"typeid": i['typeid'],
				'play': i['play'],
				'pic': i['pic'],
				'description': i['description'],
				'title': i['title'],
				'length': i['length'],
				'bv': i['bvid'],
			}
			data.append(vd)

		return {'result': '200', 'all_video': data}

	def danmu_cloud(self, bv):

		if bv[:2] in ['bv', 'BV']:
			url = 'https://www.bilibili.com/video/' + bv
			html = requests.get(url, headers=self.header)
			html.encoding = html.apparent_encoding

			# 通过正则表达式查找得到可以指向弹幕网页的链接cid
			match = r'cid=(.*)&aid'
			cid = re.search(match, html.text).group().replace('cid=', '').replace('&aid', '')

			comment_url = 'https://comment.bilibili.com/' + str(cid) + '.xml'
			comment_text = requests.get(comment_url, headers=self.header)
			comment_selector = etree.HTML(comment_text.content)
			comment_content = comment_selector.xpath('//i')
			a = []
			for comment_each in comment_content:
				comments = comment_each.xpath('//d/text()')
				if comments:
					for comment in comments:
						a.append(comment)

			import jieba.analyse
			result = jieba.analyse.textrank(','.join(a), topK=50, withWeight=True)
			keywords = dict()
			for i in result:
				keywords[i[0]] = i[1]

			wc = WordCloud(font_path='../static/simkai.ttf', background_color='White', max_words=50)
			try:
				wc.generate_from_frequencies(keywords)
				wc.to_image()
			except:
				return {'result': '弹幕过少，无法分析'}
			import base64

			def im_2_b64(image):
				buff = BytesIO()
				image.save(buff, format="PNG")
				img_str = base64.b64encode(buff.getvalue())
				img_str = str(img_str, "utf-8")
				return img_str

			img_str = im_2_b64(wc.to_image())
			res = {
				'result': '200',
				'img': img_str
			}
			return res

		else:
			return {'result': '输入有误'}

	def up_detail_2(self, mid):
		import math
		url = f'https://api.bilibili.com/x/space/arc/search?mid={mid}'
		fa = json.loads(requests.get(url, headers=self.header).text)
		tlist = fa['data']['list']['tlist']
		names = []
		count = []
		alll = int(fa['data']['page']['count'])
		oot = 0
		for i in tlist:
			if tlist[i]['count'] / alll > 0.01:
				names.append(tlist[i]['name'])
				count.append(tlist[i]['count'])
			else:
				oot += tlist[i]['count']
		names.append('其他')
		count.append(oot)

		import matplotlib.pyplot as plt
		plt.figure(figsize=(10, 8), dpi=200)
		plt.rcParams['font.sans-serif'] = ['SimHei']
		plt.pie(count[::-1], labels=names[::-1], autopct="%1.2f%%")
		plt.axis('equal')
		plt.legend(fontsize=18)
		plt.rcParams['font.size'] = '20'
		from io import BytesIO
		import base64

		figfile = BytesIO()
		plt.savefig(figfile, format='png')
		figfile.seek(0)  # rewind to beginning of file
		figdata_png = base64.b64encode(figfile.getvalue())
		img_str = str(figdata_png, "utf-8")
		data = {
			'img': img_str,
			'all': fa['data']['page']['count']
		}

		return data


def video_data_to_sqlite(mid):
	one = spyder(1)
	video_data = one.all_video(mid)['all_video']
	"""
			vd = {
				"typeid": i['typeid'],
				'play': i['play'],
				'pic': i['pic'],
				'description': i['description'],
				'title': i['title'],
				'length': i['length'],
				'bv': i['bvid'],
			}
		return {'result': '200', 'all_video': data}
	"""
	# print(video_data)
	for i in video_data:

		bv = i['bv']
		if Video.objects.filter(bv=bv).first():
			break
		else:
			vid = Video(
				type_id=i['typeid'],
				play=i['play'],
				pic=i['pic'],
				description=i['description'],
				title=i['title'],
				length=i['length'],
				bv=i['bv'],
			)
			vid.save()


def up_data_update(mid, condition='0'):
	"""
	mid,
	condition为0，数据存在则不跟新
			 为1，更新数据
	"""
	if Up.objects.filter(mid=mid).first():
		if condition == '0':
			video_data_to_sqlite(mid)
			return {'result': 'up已存在，视频信息已更新'}
		elif condition == '1':
			update_tools = spyder('up_detail')
			res = update_tools.up_detail(mid=mid)
			Up.objects.filter(mid=mid).first().delete()
			one_up = Up(
				fans=res['data']['fans'],
				up_name=res['data']['name'],
				sign=res['data']['sign'],
				image=res['data']['face'],
				mid=mid
			)
			one_up.save()
			video_data_to_sqlite(mid)
			return {'result': '数据已更新'}
	else:
		update_tools = spyder('up_detail')
		res = update_tools.up_detail(mid=mid)
		if res['result'] == '200':

			one_up = Up(
				fans=res['data']['fans'],
				up_name=res['data']['name'],
				sign=res['data']['sign'],
				image=res['data']['face'],
				mid=mid
			)
			one_up.save()
			video_data_to_sqlite(mid)
			return {'result': '数据已更新'}

		else:
			return res


def up_update(request):
	if request.method == 'GET':
		res = {'result': ''}
		return render(request, 'up_update.html', res)
	else:
		print(request.POST)
		mid = request.POST.get("mid")
		data = up_data_update(mid=mid)
		return render(request, 'up_update.html', data)


def up_detail(request):
	if request.method == 'GET':
		mid = request.GET.get('mid')

		if mid:
			one_up = Up.objects.filter(mid=mid).first()
			if one_up:
				lj = spyder('1')
				data2 = lj.up_detail_2(mid)
				res = {
					'result': '获取成功',
					'data': {
						'name': one_up.up_name,
						'fans': one_up.fans,
						'face': one_up.image,
						'sign': one_up.sign,
						'data2': data2
					},
				}
			else:
				res = {'result': '未获取该up的数据', 'data': ''}
		else:
			one_up = Up.objects.filter(mid=423895).first()

			lj = spyder('1')
			data2 = lj.up_detail_2(423895)

			res = {
				'result': '默认数据已显示',
				'data': {
					'name': one_up.up_name,
					'fans': one_up.fans,
					'face': one_up.image,
					'sign': one_up.sign,
					'data2': data2
				},
			}
		return render(request, 'up_detail.html', res)
	else:
		return render(request, '404.html')


def videos(request):
	res = {
			'result': '',
			'data': {
				'pic': '../../media/Image/default.png',
				'img': '',
				'iss': 'none'
			}
	}
	if request.method == 'GET':
		bv = request.GET.get('bv')

		one = Video.objects.filter(bv=bv).first()
		if bv:
			if one:
				tools = spyder('1')
				# img = tools.danmu_cloud(bv)['img']
				iim = tools.danmu_cloud(bv)
				if iim['result'] != '200':
					res['result'] = iim['result']
					return render(request, 'video.html', res)
				res['result'] = '数据已加载'
				res['data'] = {
					"typeid": one.type_id,
					'play': one.play,
					'pic': one.pic,
					'description': one.description,
					'title': one.title,
					'length': one.length,
					'img': tools.danmu_cloud(bv)['img'],
					'iss': 'flex'
				}
			else:
				res['result'] = '数据不存在'
		else:
			res['result'] = ''

	return render(request, 'video.html', res)


def all_up(request):
	if request.method == "GET":
		res = {
			'result': '',

		}
		cont = dict(request.GET)

		if 'content' in cont:
			from django.db.models import Q
			up_qs = Up.objects.filter(Q(mid=cont['content'][0]) | Q(up_name__contains=cont['content'][0]))
		else:
			up_qs = Up.objects.all()
		data = []
		kk = 0
		# page是需要减一的
		if "page" not in cont:
			kk = 0
		else:
			kk = int(cont['page'])

		end1 = min(len(up_qs), (kk+1)*20)

		# for one_up in up_qs[kk: end1+1]:
		for one_up in up_qs[::-1]:
			data.append({
					'name': one_up.up_name,
					'fans': one_up.fans,
					'face': one_up.image,
					'sign': one_up.sign,
					'mid': one_up.mid
			})

		return render(request, 'all_up.html', {'datas': data})
	else:
		return render(request, '404.html')

