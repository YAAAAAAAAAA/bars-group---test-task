from django import forms

class RecruitCreateForm(forms.Form):
    name = forms.CharField(label='Имя рекрута')
    age = forms.IntegerField(label='Возраст рекрута', min_value=1, max_value=10000)
    email = forms.EmailField(label='Email рекрута')
    planet_habitat = forms.CharField(label='Планета обитания рекрута')