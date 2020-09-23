from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import CoffeehouseUser

class UserCreateForm(UserCreationForm):

    #first_name = forms.CharField(max_length=100)
    age = forms.IntegerField(required=True)
    first_name=forms.CharField(required=True)
    email=forms.EmailField(required=True)
    college = forms.BooleanField(required=False,initial=True)
    c1=(('a','a'),('b','b'),('c','c'),('ab','ab'),)
    c2=(('e','e'),('f','f'),('g','g'),)
    c3=(('1','1'),('2','2'),('3','3'),)
    clgname = forms.ChoiceField(choices=c1)
    clgcourse=forms.ChoiceField(choices=c2)
    clgyear=forms.ChoiceField(choices=c3)


    class Meta:
        fields=('first_name','username','email','age','college','clgname','clgcourse','clgyear','password1','password2')
        model=CoffeehouseUser

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Dispaly Name'
        self.fields['email'].label='Email Address'

class UserUpdateForm(forms.ModelForm):
    age = forms.IntegerField()
    first_name=forms.CharField()
    email=forms.EmailField()
    college = forms.BooleanField(required=False)
    c1=(('a','a'),('b','b'),('c','c'),('ab','ab'),)
    c2=(('e','e'),('f','f'),('g','g'),)
    c3=(('1','1'),('2','2'),('3','3'),)
    clgname = forms.ChoiceField(choices=c1)
    clgcourse=forms.ChoiceField(choices=c2)
    clgyear=forms.ChoiceField(choices=c3)

    class Meta:
        model=CoffeehouseUser
        fields=['first_name','username','email','age','college','clgname','clgcourse','clgyear']

class PicUpdateForm(forms.ModelForm):
    #image=forms.ImageField(initial=default)
    image = forms.ImageField(widget=forms.FileInput,)

    class Meta:
        model=CoffeehouseUser
        fields=['image']

class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
            )




