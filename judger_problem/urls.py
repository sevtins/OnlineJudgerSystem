from django.contrib import admin
from django.urls import path
from . import views

app_name = "problem"

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("list/", views.ProblemList.as_view(), name="problemList"),
    path("detail/<int:problem_id>/", views.ProblemDetail.as_view(), name="problemdetail"),
]
