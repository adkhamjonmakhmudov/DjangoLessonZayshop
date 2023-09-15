from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from apps.models import User


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)  # None

        if user is None:
            raise ValidationError('Parol yoki foydalanuvchi nomi togri kelmayapti')
        return cleaned_data

    '''
    authenticate-. Bu funksiya, foydalanuvchi to'g'ri ma'lumotlar kiritgandagina avtomatik ravishda kirishni amalga oshiradi.
    Cross Site Request Forgery - (CSRF) foydalanuvchining shaxsiy ma'lumotlarini himoya qilish maqsadida amalga oshiriladi
    Bu token, foydalanuvchi brauzeridan kelgan so'roq ma'lumotlarini serverga yuborishda xavfsizlikni ta'minlash uchun foydalaniladi.    
    '''
