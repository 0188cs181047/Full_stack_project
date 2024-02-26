from django.contrib import admin
from .models import Course ,Question ,Result ,UploadedExcel
# Register your models here.


class adminCource(admin.ModelAdmin):
    list_display = ("course_name" ,"question_number","total_marks")

class adminQuestions(admin.ModelAdmin):
    list_display = ("course" ,"marks" ,"question" ,"option1" ,"option2" ,"option3" ,"option4" ,"answer")


admin.site.register(Course,adminCource )
admin.site.register(Question ,adminQuestions)
admin.site.register(Result)
admin.site.register(UploadedExcel)
