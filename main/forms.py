import re

from django import forms
from django.contrib.auth.models import User

from .models import Application, CourseReview, UserProfile


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', min_length=6, max_length=30)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    full_name = forms.CharField(label='ФИО', max_length=150)
    phone = forms.CharField(label='Номер телефона', max_length=30)
    email = forms.EmailField(label='E-mail')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_username(self):
        username = self.cleaned_data['username']
        # Логин принимается только в формате латинских букв и цифр.
        if not re.fullmatch(r'[A-Za-z0-9]+', username):
            raise forms.ValidationError('Логин должен содержать только латинские буквы и цифры.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def save(self):
        # После создания пользователя сразу сохраняем данные его личного кабинета.
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        UserProfile.objects.create(
            user=user,
            full_name=self.cleaned_data['full_name'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
        )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        # В заявке пользователь выбирает курс, дату, время и способ оплаты.
        fields = ['course', 'start_date', 'start_time', 'payment_method']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = 'form-select' if name in ('course', 'payment_method') else 'form-control'
            field.widget.attrs.update({'class': css_class})


class CourseReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        label='Оценка',
        choices=[(i, str(i)) for i in range(1, 6)],
    )

    class Meta:
        model = CourseReview
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Поделитесь впечатлениями о курсе и очном обучении'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].widget.attrs.update({'class': 'form-select'})
