from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView
from .models import TestSet, Answers, Questions
from testoviy_test.settings import collections_name
from copy import deepcopy


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = "register.html"


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"


def tests(request):
    test = TestSet.objects.all()
    return render(request, "index.html", {"test": test})


class TestView(ListView):
    model = TestSet
    template_name = "test.html"
    context_object_name = "questions"

    def get(self, request, *args, **kwargs):
        user = str(self.request.user)
        doc = collections_name.find_one({"_id": user})

        if not doc:
            collections_name.insert_one({"_id": user})
            collections_name.update_one({"_id": user}, {"$set": doc})

        elif kwargs["slug"] not in doc.keys():
            doc[kwargs["slug"]] = {}
            doc[kwargs["slug"]]["score"] = 0
            collections_name.update_one({"_id": user}, {"$set": doc})

        return super().get(self, request, *args, **kwargs)

    def post(self, *args, **kwargs):
        data = self.request.POST
        answers = Answers.objects.filter(questions_id=data["questions_id"], is_correct=True).values_list("text")
        user = str(self.request.user)
        test_name = kwargs["slug"]

        user_answers = []
        for i in data:
            if i in ["csrfmiddlewaretoken", "questions_id", "questions", "end"]:
                continue
            user_answers.append(i)

        user_answers_copy = deepcopy(user_answers)

        if len(answers) == len(user_answers):
            for i in answers:
                if i[0] in user_answers:
                    user_answers_copy.remove(i[0])

        doc = collections_name.find_one({"_id": user})

        if not user_answers_copy:
            list_answers = []

            for i in answers:
                list_answers.append(i[0])
            doc[test_name][data["questions"]] = list_answers
            doc[test_name]["score"] += 1

        else:
            doc[test_name][data["questions"]] = user_answers

        collections_name.update_one({"_id": user}, {"$set": doc})

        if data["end"] == "True":
            return HttpResponseRedirect(f"/result/{self.kwargs['slug']}")
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.path.split("/")
        context["test_name"] = self.kwargs["slug"]

        context["next"] = next_url[2] + "/" + str(int(next_url[3]) + 1)

        if len(context["questions"]) == self.kwargs["question"]:
            context["next"] = next_url[2] + "/" + str(int(next_url[3]))
            user = collections_name.find_one({"_id": str(self.request.user)})
            context["score"] = user[self.kwargs["slug"]]["score"]

        context["questions"] = context["questions"][self.kwargs["question"] - 1]

        return context

    def get_queryset(self):
        test = TestSet.objects.filter(slug=self.kwargs["slug"]).first()
        return test.questions.get_queryset()


class ResultView(ListView):
    model = TestSet
    template_name = "result.html"
    context_object_name = "result"

    def post(self, *args, **kwargs):
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = collections_name.find_one({"_id": str(self.request.user)})
        context["score"] = user[self.kwargs["slug"]]["score"]
        return context


def logout_user(request):
    logout(request)
    return redirect("login")
