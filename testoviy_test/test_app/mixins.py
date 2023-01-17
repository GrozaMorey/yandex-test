from .models import TestSet


class TestSetQueryMixin:

    def get_test_queryset(self, **kwargs):
        test = TestSet.objects.filter(slug=kwargs["slug"]).first()
        return test.questions.get_queryset()
