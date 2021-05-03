from django import forms
from .models import Post, Profile, PostImage, Comment
from django.contrib.auth.models import User


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = [
            'image'
        ]

        labels = {
            'image': 'Photo'
        }

        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True})
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Comment here!!!',
                                                                     'rows': '4', 'cols': '50'}))

    class Meta:
        model = Comment
        fields = ('content',)


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'status',
            'restrict_comments',
        ]


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'status',
            'restrict_comments',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def clean_password2(self):
        password = self.cleaned_data.get("password1")
        confirm_password = self.cleaned_data.get("password2")

        if confirm_password != password:
            raise forms.ValidationError(
                "password mismatch"
            )
        if len(confirm_password) < 8:
            raise forms.ValidationError('password must be at least 8 characters')
        return confirm_password

    # def clean_confirm_password(self):
    #     password = self.cleaned_data.get("password")
    #     confirm_password = self.cleaned_data.get("confirm_password")
    #
    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "password mismatch"
    #         )
    #     if len(password) < 8:
    #         raise forms.ValidationError('password must be at least 8 characters')
    #     return confirm_password
