from django.db import models


# Create your models here.

class Problem(models.Model):
    """
    作业题目的数据模型
    """
    title = models.CharField(max_length=128, verbose_name="题目标题")
    problem_content = models.TextField(verbose_name="题目内容")
    problem_input = models.CharField(max_length=128, verbose_name="样例输入")
    problem_output = models.CharField(max_length=128, verbose_name="样例输出")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建题目时间")
    author = models.CharField(max_length=128, verbose_name="作者")


class SubmitStatus(models.Model):
    """
    判题状态的数据模型
    """
    fk_problem_id = models.ForeignKey(Problem, verbose_name="外键题目id")
    user_code_dir = models.CharField(verbose_name="用户代码路径")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="提交代码时间")
    author = models.CharField(max_length=128, verbose_name="作者")
