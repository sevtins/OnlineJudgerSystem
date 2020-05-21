from django.contrib import admin
from django.urls import path
from .views import ProblemList

app_name = "problem"

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("list/", ProblemList.as_view(), name="problemList")
]
