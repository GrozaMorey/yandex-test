from django.contrib.auth.models import User
from django.test import TestCase, Client
from .models import TestSet, Questions, Answers
from testoviy_test.settings import collections_name
from django.contrib import auth
from .views import *


# TODO Проверки на правильный шаблон
class UrlTest(TestCase):

    def setUp(self):
        test = TestSet(title="test", slug="test")
        test.save()
        question = Questions(text="test", test=test)
        question.save()
        answers = Answers(text="test", questions=question)
        answers.save()
        user = User.objects.create(username='test')
        user.set_password('12345')
        user.save()

        collections_name.insert_one({"_id": "test", "test": {"score": 0, "complete": False}})

    def tearDown(self):
        collections_name.delete_one({"_id": "test"})

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test', password='12345')
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)

    def test_register_page(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_desc_page(self):
        response = self.client.get("/test/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test', password='12345')
        response = self.client.get("/test/")

        self.assertEqual(response.status_code, 200)

    def test_test_question_page(self):
        response = self.client.get("/test/1/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test', password='12345')
        response = self.client.get("/test/1/")

        self.assertEqual(response.status_code, 200)

    def test_result_page(self):
        response = self.client.get("/result/test/")
        self.assertEqual(response.status_code, 302)

        self.client.login(username='test', password='12345')

        user = collections_name.find_one({"_id": "test"})
        user["test"]["complete"] = True
        collections_name.update_one({"_id": "test"}, {"$set": user})

        response = self.client.get("/result/test/")
        self.assertEqual(response.status_code, 200)


class ModelTest(TestCase):
    def setUp(self):
        test = TestSet(title="test", slug="test")
        test.save()
        question = Questions(text="test", test=test)
        question.save()
        answers = Answers(text="test", questions=question)
        answers.save()
        user = User.objects.create(username='test')
        user.set_password('12345')
        user.save()

    def test_test_set(self):
        test = TestSet.objects.get(title="test")
        self.assertTrue(test)


class ViewTest(TestCase):

    def setUp(self):
        test = TestSet(title="test", slug="test")
        test.save()
        question = Questions(text="test", test=test)
        question.save()
        answers = Answers(text="test", is_correct=True, questions=question)
        answers.save()
        user = User.objects.create(username='test')
        user.set_password('12345')
        user.save()

    def tearDown(self):
        collections_name.delete_one({"_id": "test"})

    def test_test_view(self):
        self.client.login(username="test", password="12345")
        collections_name.insert_one({"_id": "test", "test": {"score": 0, "complete": False}})

        response = self.client.get("/test/1/")

        self.assertEqual(response.context["next"], "test/1")
        self.assertEqual(response.context["score"], 0)
        self.assertEqual(response.context["test_name"], "test")
        self.assertEqual(response.context["questions"], Questions.objects.get(text="test"))

        data = {"test": "on", "questions_id": f"{Questions.objects.first().id}", "end": True, "questions": "test"}
        response = self.client.post("/test/1/", data=data)

        mongo = collections_name.find_one({"_id": "test"})
        self.assertEqual(mongo["test"]["score"], 1)
        self.assertEqual(mongo["test"]["complete"], True)
        self.assertIsNotNone(mongo["test"]["test"])
        self.assertEqual(response.status_code, 302)

    def test_result_view(self):
        self.client.login(username="test", password="12345")
        collections_name.insert_one({"_id": "test", "test": {"score": 1, "complete": True}})

        response = self.client.get("/result/test/")

        self.assertEqual(response.context["score"], 1)
        self.assertEqual(response.context["total_questions"], 1)
        self.assertEqual(response.context["percent"], 100)
        self.assertEqual(response.context["slug"], "test")

        collections_name.delete_one({"_id": "test"})
        collections_name.insert_one({"_id": "test", "test": {"score": 0, "complete": True}})

        response = self.client.get("/result/test/")

        self.assertEqual(response.context["percent"], 0)

    def test_desk_view(self):
        self.client.login(username="test", password="12345")
        collections_name.insert_one({"_id": "test", "test": {"score": 0, "complete": True}})
        response = self.client.get("/test/")

        self.assertEqual(response.status_code, 302)
