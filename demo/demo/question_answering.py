from django.shortcuts import render


def question_answering(request):  # index页面需要一开始就加载的内容写在这里
	context = {}
	return render(request, 'question_answering.html', context)