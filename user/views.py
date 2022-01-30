import requests
from django.shortcuts import render
from django.http import JsonResponse
from user.models import *
import json


# Create your views here.
def home(request):
	ups = Up.objects.all()
	data = []
	for one_up in ups[::-1][:8]:
		data.append({
				'name': one_up.up_name,
				'fans': one_up.fans,
				'face': one_up.image,
				'date': one_up.update_time,
				'mid': one_up.mid,
		})
	dic = {
		'1': '动画',
		'13': '番剧',
		'167': '国创',
		'3': '音乐',
		'129': '舞蹈',
		'4': '游戏',
		'36': '知识',
		'188': '科技',
		'234': '运动',
		'223': '汽车',
		'160': '生活',
		'211': '美食',
		'217': '动物圈',
		'119': '鬼畜',
		'155': '时尚',
		'202': '资讯',
		'5': '娱乐',
		'181': '影视',
		'177': '纪录片',
		'23': '电影',
		'11': '电视剧'
	}

	import matplotlib.pyplot as plt
	plt.figure(figsize=(10, 8), dpi=200)
	plt.rcParams['font.sans-serif'] = ['SimHei']

	dada = json.loads(requests.get('https://api.bilibili.com/x/web-interface/online').text)['data']['region_count']
	for i in list(dada.keys()):
		if i not in dic:
			dada.pop(i)
	dada = list(dada.items())

	dada = sorted(dada, key=lambda x: x[1], reverse=True)[:7]

	plt.bar([dic[i[0]] for i in dada], [i[1] for i in dada])
	plt.legend(fontsize=20)
	plt.rcParams['font.size'] = '20'
	from io import BytesIO
	import base64

	figfile = BytesIO()
	plt.savefig(figfile, format='png')
	figfile.seek(0)  # rewind to beginning of file
	figdata_png = base64.b64encode(figfile.getvalue())
	img_str = str(figdata_png, "utf-8")
	return render(request, 'index.html', {'datas': data, 'count': Up.objects.count(), 'img': img_str})


def is_login(request):
	if request.session is None:
		request.session['condition'] = '0'
		request.session['name'] = '看看左图'
		request.session['default_img'] = '../../media/Image/default.png'

	data = {
		"name1": request.session['name'],
		"srcc": request.session['default_img']
	}
	# print(data)
	return JsonResponse(data, safe=False)


def login(request):
	result = {
		'result': ''
	}
	print(request.method)
	if request.method == 'GET':
		if request.GET:
			if request.GET.get('ccd') == '1':

				request.session['condition'] = '0'
				request.session['name'] = '看看左图'
				request.session['default_img'] = '../../media/Image/default.png'
				result['result'] = '退出成功'

		return render(request, 'login.html', result)
	else:

		name = request.POST.get('name')
		password = request.POST.get('password')

		one = User.objects.filter(nickname=name).first()

		if one:
			if one.password == password:
				result['result'] = '登陆成功'
				request.session['condition'] = "1"
				request.session['name'] = name
				request.session['default_img'] = one.image.url
			else:
				result['result'] = '密码错误'
		else:
			result['result'] = '用户名不存在'
			if not name:
				result['result'] = '退出成功'

		return render(request, 'login.html', result)
