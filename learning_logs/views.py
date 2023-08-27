from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm
from .forms import EntryForm

def index(request):
	''' Домашняя страница приложения Learning Log '''
	return render(request, 'learning_logs/index.html')


@login_required
def topics(request):
	''' Страница со списком всех тем '''
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics': topics}

	return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
	""" Выводит одну тему и все ее записи """
	topic = Topic.objects.get(id=topic_id)
	_check_topic_owner(request, topic)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic': topic, 'entries': entries}
	return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
	""" Определяет новую тему """
	if request.method != "POST":
		#  Данные не отправлялись, создается пустая форма
		form = TopicForm()
	else:
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			print(new_topic.owner)
			new_topic.save()
			return redirect('learning_logs:topics')

	# Вывод пустой строки или недействительной формы
	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
	""" Определение новых записей """
	topic = Topic.objects.get(id=topic_id)
	_check_topic_owner(request, topic)
	if request.method != "POST":
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return redirect('learning_logs:topic', topic_id=topic_id)
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
	""" Редактирование записей """
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	_check_topic_owner(request, topic)
	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic', topic_id=topic.id)
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def delete_topic(request, topic_id):
	""" Удаление статьи """
	topic = Topic.objects.get(id=topic_id)
	_check_topic_owner(request, topic)
	topic.delete()
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}

	return render(request, 'learning_logs/topics.html', context)


def _check_topic_owner(request, topic):
	""" Проверяет user на владение файла, если user не является владельцем, то
	возвращает ошибку Http404 """
	if request.user != topic.owner:
		raise Http404
