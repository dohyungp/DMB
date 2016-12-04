from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,

)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='아이디')
    password = forms.CharField(widget=forms.PasswordInput, label='비밀번호')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("아이디와 패스워드를 확인해주세요.")
            if not user.is_active:
                raise forms.ValidationError("이 사용자는 로그인 중입니다.")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='이메일 주소')
    email2 = forms.EmailField(label='이메일 확인')
    password = forms.CharField(widget=forms.PasswordInput, label='비밀번호')
    password_ck = forms.CharField(widget=forms.PasswordInput, label='비밀번호 확인')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            'password_ck',

        ]
    # def clean(self, *args, **kwargs):
    #     email = self.cleaned_data.get('email')
    #     email2 = self.cleaned_data.get('email2')
    #     if email != email2:
    #         raise forms.ValidationError("이메일이 맞지 않습니다.")
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs.exists():
    #         raise forms.ValidationError("이 이메일은 이미 회원가입되어 있습니다.")
    #     return super(UserRegisterForm, self).clean(*args, **kwargs)

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        print(email, email2)
        if email != email2:
            raise forms.ValidationError("이메일이 맞지 않습니다.")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("이 이메일은 이미 회원가입되어 있습니다.")
        return email

    def clean_password2(self):
        print(self.cleaned_data)
        password = self.cleaned_data.get('password')
        password_ck = self.cleaned_data.get('password_ck')
        print(password, password_ck)
        if password != password_ck:
            raise forms.ValidationError("비밀번호가 맞지 않습니다.")
        return password