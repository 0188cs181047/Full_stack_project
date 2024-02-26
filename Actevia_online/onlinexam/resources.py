
from import_export import resources
from import_export.widgets import ForeignKeyWidget
from .models import Question ,Course
from import_export.fields import Field

class CourceSuorce(resources.ModelResource):
    class Meta:
        model = Course


class QuestionSource(resources.ModelResource):
    course =Field(column_name='course', attribute='course', widget=ForeignKeyWidget(Course, 'course_name'))
    class Meta:
        model = Question
        import_id_fields = ('id', 'marks','question','option1','option2' ,'option3','option4' ,'answer')
        fields = ('id','course','marks','question','option1','option2' ,'option3','option4' ,'answer')


