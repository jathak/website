from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import login
from django.template import Context, Template
from django.forms import *
from django.core.serializers.json import DjangoJSONEncoder
import json, re
from users.models import *
from website.models import *

def index(request):
    template = loader.get_template('website/index.html')
    officers = UserProfile.objects.filter(user_type=3, approved=True)
    # context = RequestContext(request, { 'officers': officers })
    # return HttpResponse(template.render(context))
    return render(request, 'website/index.html', { 'officers': officers })

def oh(request):
    return render(request, 'website/oh.html', {})

def interview(request):
	question_categories = QuestionCategory.objects.order_by("category_title")
	return render(request, 'website/interview.html', {"question_categories": question_categories})

def question_cat(request):
	cat_id = request.GET.get("cat_id")
	questions = Question.objects.filter(question_category__id=cat_id).order_by("question_difficulty")
	question_titles = [question.question_title for question in questions]
	question_ids = [question.id for question in questions]
	data = {"question_titles": question_titles, "question_ids": question_ids}
	# questions = [question.question_title for question in \
	# 	Question.objects.filter(question_category__id=cat_id).order_by("question_difficulty")]
	questions_list = json.dumps(data)
	return HttpResponse(questions_list, content_type="application/json")
