from django.db import models
from django.contrib.auth.models import User


class ProblemLabel(models.Model):
    """
    题目标签的数据模型
    """

    name = models.CharField(max_length=128, verbose_name="标签名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="标签创建题目时间")
    fk_author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="作者")

    class Meta:
        verbose_name = verbose_name_plural = "题目标签"

    def __str__(self):
        return self.name


class Problem(models.Model):
    """
    作业题目的数据模型
    """

    @classmethod
    def get_problem_list(cls):
        return cls.objects.all().only("title", "fk_author", "difficulty", "explains", "Submits",
                                      "corrects")

    diff = [
        (0, "简单"),
        (1, "中等"),
        (2, "困难"),
    ]
    title = models.CharField(max_length=128, verbose_name="题目标题")
    problem_content = models.TextField(verbose_name="题目内容")
    problem_input = models.CharField(max_length=128, verbose_name="样例输入")
    problem_output = models.CharField(max_length=128, verbose_name="样例输出")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建题目时间")
    difficulty = models.IntegerField(null=True, choices=diff, verbose_name="难度")
    explains = models.IntegerField(default=0, verbose_name="题目题解数量")
    fk_labels = models.ManyToManyField(to=ProblemLabel, verbose_name="题目标签")
    Submits = models.IntegerField(default=0, verbose_name="总的用户提交次数")
    corrects = models.IntegerField(default=0, verbose_name="总的用户正确次数")
    # TODO 这里不需要联机删除，但是没有on_delete参数不行
    fk_author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="作者")

    class Meta:
        verbose_name = "题目列表"
        verbose_name_plural = "题目列表"


class SubmitStatus(models.Model):
    """
    判题状态的数据模型
    """
    fk_problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name="外键题目id")
    user_code_content = models.CharField(default="", max_length=128, verbose_name="用户代码")
    user_code_status = models.CharField(default="", max_length=56, verbose_name="提交状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="提交代码时间")
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="作者")

    class Meta:
        verbose_name_plural = "提交状态"
        verbose_name = "提交状态"
