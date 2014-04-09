#-*- Encoding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

class logininForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))

class signupForm(forms.Form):
	""" por algun motivo no funciona """
	class Meta:
		model = User
		fields = ['username', 'password']
		widget = {
			'password' : forms.PasswordInput(render_value=False),
		}
