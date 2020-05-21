from django.contrib import admin
from .models import Problem, SubmitStatus, ProblemLabel

# Register your models here.
admin.site.register(Problem)
admin.site.register(SubmitStatus)
admin.site.register(ProblemLabel)
