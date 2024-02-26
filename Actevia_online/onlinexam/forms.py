from django import forms

from .models import Course ,Question


class TeacherSalaryForm(forms.Form):
    salary=forms.IntegerField()

class Courceform(forms.ModelForm):
    class Meta:
        model = Course
        fields=['course_name','question_number','total_marks']


        widgets = {
        'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cource Name'}),
        'question_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Questions Number'}),
        'total_marks': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Marks'}),
        

    }

class QuestionForm(forms.ModelForm):
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Course Name", to_field_name="id")
    class Meta:
        model = Question
        fields ="__all__"
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

class UploadForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    file = forms.FileField()
    def clean_file(self):
        file = self.cleaned_data['file']
        if file.content_type not in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            raise forms.ValidationError('Invalid file format. Only Excel files are allowed.')
        return file
    