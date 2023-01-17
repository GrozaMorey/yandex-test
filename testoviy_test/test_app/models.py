from django.db import models
from transliterate import slugify
from django.contrib.auth.forms import UserCreationForm
from testoviy_test.settings import collections_name

class TestSet(models.Model):
    title = models.CharField(
        max_length=100,
        null=True
    )

    descriptions = models.CharField(
        max_length=1000,
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

class UserRegistration(UserCreationForm):

    def save(self):
        collections_name.insert_one({"_id": self.cleaned_data["username"]})
        return super().save()