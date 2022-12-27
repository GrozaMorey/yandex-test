from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from .models import Answers, Questions, TestSet
from .forms import QuestionForm


class AnswersInLines(NestedTabularInline):
    model = Answers
    extra = 0


class QuestionInLines(NestedStackedInline):
    model = Questions
    inlines = (AnswersInLines,)
    extra = 1


    def get_extra(self, request, obj=None, **kwargs):
        if request.path.split("/")[-2] == "change":
            return 0
        return self.extra


class TestSetAdmin(NestedModelAdmin):
    inlines = (QuestionInLines,)
    form = QuestionForm


admin.site.register(TestSet, TestSetAdmin)
