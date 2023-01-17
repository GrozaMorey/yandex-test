from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    path("register/", RegisterUser.as_view()),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user),
    path("<slug:slug>/", login_required(DescView.as_view(), login_url='/login/')),
    path("<slug:slug>/<int:question>/", login_required(TestView.as_view(), login_url='/login/')),
    path("", login_required(tests, login_url='/login/')),
    path("result/<slug:slug>/", login_required(ResultView.as_view(), login_url='/login/'), name="result")
    ]