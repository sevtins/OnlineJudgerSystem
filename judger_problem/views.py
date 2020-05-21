from django.shortcuts import render
from django.views import View

from .models import Problem


class ProblemList(View):
    """
    题目列表视图
    """

    def get(self, request):
        proble_lists = Problem.get_problem_list()
        context = {
            "proble_lists": proble_lists
        }
        return render(request, template_name="judger_problem/templates/problem_list.html", context=context)
