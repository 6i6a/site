from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
	""" Регистрирует нового пользователя """
	if request.method != "POST":
		# Пустая форма
		form = UserCreationForm()
	else:
		form = UserCreationForm(data=request.POST)
		#Обработка заполненной формы
		if form.is_valid():
			new_user = form.save()
			login(request, new_user)
			return redirect('learning_logs:index')

	context = {'form': form}
	return render(request, 'registration/register.html', context)
