from django import forms
from django.forms import (formset_factory, modelformset_factory)

from .models import (Quiz, Question, Category)

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

class BookForm(forms.Form):
    name = forms.CharField(
        label='Book Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
        })
    )


class BookModelForm(forms.ModelForm):

    class Meta:
        model = Quiz
        fields = ('name', )
        labels = {
            'name': 'Book Name'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Book Name here'
                }
            )
        }


BookFormset = formset_factory(BookForm)
BookModelFormset = modelformset_factory(
    Quiz,
    fields=('name', ),
    extra=1,
    widgets={
        'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
            }
        )
    }
)

AuthorFormset = modelformset_factory(
    Question,
    fields=('question', 'choice1'),
    extra=2,
    widgets={'question': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Author Name here'
        }),
            'choice1': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Author Name here'
        })
    }
)
