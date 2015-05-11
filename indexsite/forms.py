from django import forms
from indexsite.models import rssfeeds, rssnews, usersrss
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.rsstitle

class rssnewsAdminForm(forms.ModelForm):
    rssfeed = CustomModelChoiceField(queryset=rssfeeds.objects.all()) 
    class Meta:
        model = rssnews
        fields = '__all__'

class UserForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your nickname'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder': 'Password again'}))
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate email')
    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user

class usersrssAdminForm(forms.ModelForm):
    feed = CustomModelChoiceField(queryset=rssfeeds.objects.all()) 
    class Meta:
        model = usersrss
        fields = '__all__'

class usersrssAddForm(forms.ModelForm):
    rssfeed = forms.URLField(label='Channel URL')
    class Meta:
        model = rssfeeds
        fields = ('rssfeed',)

