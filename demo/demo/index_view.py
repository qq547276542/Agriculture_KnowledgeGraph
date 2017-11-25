# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf

import sys
sys.path.append("..")
from neo4jModel.models import Neo4j

def index(request):
	context = {}
	return render(request, 'index.html', context)
	