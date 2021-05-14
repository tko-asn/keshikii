from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model


class UserAdminCreationForm(forms.ModelForm):
    """管理サイトのユーザー作成フォーム"""

    password1 = forms.CharField(
        label='パスワード', 
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='確認用パスワード', 
        widget=forms.PasswordInput,
    )
    class Meta:
        model = get_user_model()
        fields = ('username',)
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('確認用パスワードが一致しません。')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """管理サイトのユーザー編集用フォーム"""

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'is_active', 'is_staff', 'is_superuser', 
            'password'
        )

    def clean_password(self):
        return self.initial['password']
