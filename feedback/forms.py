from django import forms


class NegativeMessageForm(forms.Form):
    phone = forms.CharField(label="Номер телефона", max_length=100)
    text = forms.CharField(label="Текст сообщения", max_length=500)
