from django import forms
from .models import Student

from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super().clean()

        start_year = cleaned_data.get("start_year")
        end_year = cleaned_data.get("end_year")

        if start_year and end_year:

            if end_year < start_year:
                raise forms.ValidationError(
                    "End year must be greater than or equal to start year."
                )

        return cleaned_data

    class Meta:
        model = Student
        fields = "__all__"


