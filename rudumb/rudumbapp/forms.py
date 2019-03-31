from django import forms
from .models import Category, Question, Quiz



class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='Username',
        max_length=32
    )
    email = forms.CharField(
        required=True,
        label='Email',
        max_length=32,
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        required=True,
        label='Password',
        max_length=32,
        widget=forms.PasswordInput()
    )


class QuizCreationForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields=['name','category', 'image']

        


    
class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=['question','choice1','choice2','choice3','choice4', 'answer']
        exclude = ("quiz",)

        labels = {
            'question' : 'Question',
            'choice1' : 'First answer',
            'choice2' : 'Second answer',
            'choice3' : 'Third answer',
            'choice4' : 'Fourth answer',
            'answer' : 'Right answer number',
        }
        widgets = {
            'question': forms.TextInput(attrs={'required': True}),
            'choice1': forms.TextInput(attrs={'required': True}),
            'choice2': forms.TextInput(attrs={'required': True}),
            'choice3': forms.TextInput(attrs={'required': False}),
            'choice4': forms.TextInput(attrs={'required': False}),
            'answer': forms.NumberInput(attrs={'required': True}),

        }