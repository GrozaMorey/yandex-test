from django.db import models
from transliterate import slugify


class TestSet(models.Model):
    title = models.CharField(
        max_length=100,
        null=True
                             )

    slug = models.CharField(
        max_length=120,
        auto_created=True,
        default=None,
        editable=False
                            )
    def __str__(self):
        return self.title

    def clean(self):
        self.slug = slugify(self.title)



class Questions(models.Model):
    text = models.CharField(max_length=200,
                            null=False)

    test = models.ForeignKey(TestSet,
                             on_delete=models.CASCADE,
                             related_name="questions")


    def __str__(self):
        return self.text


class Answers(models.Model):
    text = models.CharField(max_length=200,
                            null=False)

    is_correct = models.BooleanField(default=False)

    questions = models.ForeignKey(Questions,
                                  on_delete=models.CASCADE,
                                  related_name="answers")

    def __str__(self):
        return self.text
