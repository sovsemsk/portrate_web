from django.forms import Form, CharField, PasswordInput


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)

    # Конструктор формы
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "bp5-input"
        self.fields["username"].widget.attrs["placeholder"] = "Логин"
        self.fields["password"].widget.attrs["class"] = "bp5-input"
        self.fields["password"].widget.attrs["placeholder"] = "Пароль"
