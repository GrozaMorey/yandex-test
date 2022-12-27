from django.urls import path

from .views import *

urlpatterns = [
    path("register/", RegisterUser.as_view()),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user),
    path("test/<slug:slug>/<int:question>/", TestView.as_view()),
    path("test/", tests),
    path("result/<slug:slug>/", ResultView.as_view(), name="result")
]