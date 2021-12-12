from django import forms

from school.models import ClassName, MyUser

class_names = ClassName.objects.values_list('class_name')

GEEKS_CHOICES = (
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)


class Register(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.IntegerField()
    dob = forms.DateField()
    status = forms.BooleanField()
    email = forms.EmailField()
    image = forms.ImageField()
    password = forms.CharField(widget=forms.PasswordInput)
    conform_password = forms.CharField(widget=forms.PasswordInput)
    class_name = forms.ChoiceField(choices=GEEKS_CHOICES)


class UpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'phone', 'dob', 'status', 'image', 'password', 'class_name']
