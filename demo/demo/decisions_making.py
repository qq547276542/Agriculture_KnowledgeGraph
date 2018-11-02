from django.shortcuts import render


def decisions_making(request):  # index页面需要一开始就加载的内容写在这里
	context = {}
	return render(request, 'decisions_making.html', context)