from django import forms

from students.models import Student


# from django.core.exceptions import ValidationError

class StudentForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Student
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone_number', 'address', 'gender', 'dob']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = "form-control"
        self.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        self.fields['middle_name'].widget.attrs['class'] = "form-control"
        self.fields['middle_name'].widget.attrs['placeholder'] = "Middle Name"
        self.fields['last_name'].widget.attrs['class'] = "form-control"
        self.fields['last_name'].widget.attrs['placeholder'] = "Last Name"
        self.fields['phone_number'].widget.attrs['class'] = "form-control"
        self.fields['phone_number'].widget.attrs['placeholder'] = "Phone Number"
        self.fields['dob'].widget.attrs['class'] = "form-control"
        self.fields['gender'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['class'] = "form-control"
        self.fields['email'].widget.attrs['placeholder'] = "Email Address"
        self.fields['address'].widget.attrs['class'] = "form-control"
        self.fields['address'].widget.attrs['placeholder'] = "Address"
