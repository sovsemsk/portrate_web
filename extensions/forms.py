from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "bp5-input"
        self.fields["username"].widget.attrs["placeholder"] = "логин"
        self.fields["password"].widget.attrs["class"] = "bp5-input"
        self.fields["password"].widget.attrs["placeholder"] = "пароль"
