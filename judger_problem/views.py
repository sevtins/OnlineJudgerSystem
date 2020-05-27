import json

from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests

from .models import Problem, SubmitStatus


# from .forms import SubmitForm

@method_decorator(login_required, name="dispatch")
class ProblemList(View):
    """
    题目列表视图
    """

    def get(self, request):
        proble_lists = Problem.get_problem_list()

        # 已解决题目数量
        solve_count = len(SubmitStatus.objects.filter(user_code_status="正确", author=request.user))
        # 未解决题目数量
        problem_count = Problem.objects.count() - solve_count

        context = {
            "proble_lists": proble_lists,
            "problem_count": problem_count,
            "solve_count": solve_count,
        }
        return render(request, template_name="judger_problem/templates/problem_list.html", context=context)


@method_decorator(login_required, name="dispatch")
class ProblemDetail(View):
    """
    展示题目详情的视图
    """

    def get(self, request, *args, **kwargs):
        """
        处理get请求，返回题目详情页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        problem = Problem.objects.filter(id=kwargs["problem_id"])[0]
        context = {
            "problem_content": problem
        }
        return render(request=request, template_name="judger_problem/templates/problem_detail.html", context=context)

    def post(self, request, *args, **kwargs):
        """
        处理代码提交请求
        :param request: request.POST['user_code']包含用户代码
        :param kwargs: kwargs["problem_id"]提交的代码对应题号
        :return: 返回get请求同样的内容外，还返回用户代码提交结果信息mess,
                 以及status; error:表示用户代码无法运行, success:表示用户代码可以运行但是输出不一定正确
        """

        # 获取model对象problem
        problem = Problem.objects.filter(id=kwargs["problem_id"])[0]
        context = {
            "problem_content": problem,
            "mess": "",
        }

        # 将用户代码和输入数据打包成data
        # 向判题服务器发起post请求
        # 将判题服务器结果转为json格式
        user_code = request.POST['user_code']
        data = {
            "user_code": user_code,
            "user_input": problem.problem_input,
        }

        # 设置提交状态
        submit_status = SubmitStatus()
        submit_status.fk_problem_id = problem
        submit_status.user_code_content = user_code
        submit_status.author = request.user

        # TODO ip地址应该写进环境变量中
        result = requests.post("http://120.92.173.80:8080/", data=data)
        # result = str(result, "utf-8")
        result = json.loads(result.text)

        # 用户代码不可以运行
        if result["status"] == "error":
            context["status"] = "error"
            context["mess"] = "代码无法运行"
            submit_status.user_code_status = "代码无法运行"
            submit_status.save()
            return render(request, template_name="judger_problem/templates/problem_detail.html", context=context)

        # 用户代码可运行，检测答案是否正确
        if problem.problem_output == result["output"]:
            context["status"] = "success"
            context["mess"] = "答案正确"
            submit_status.user_code_status = "正确"
        else:
            context["status"] = "success"
            context["mess"] = "答案错误，请检查你的代码逻辑"
            submit_status.user_code_status = "错误"
        submit_status.save()
        return render(request, template_name="judger_problem/templates/problem_detail.html", context=context)
