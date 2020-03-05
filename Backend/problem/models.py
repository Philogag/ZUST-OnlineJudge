from django.db import models
from enum import IntEnum



class SHOW_MOD(IntEnum):
    HIDE = 0
    SHOW = 1
    IN_CONTEST = 2

class JUDGE_METHOD(IntEnum):
    Local = 0
    HDU = 1
    Codeforce = 2

to_choices = lambda enum: tuple([(int(v), str(v).split(".")[1]) for v in enum])

class Problem(models.Model):
    judge_method = models.IntegerField(choices=to_choices(JUDGE_METHOD), default=0) # 判题方法
    real_pid = models.IntegerField() # 真实问题id，local状态下等于id
    writer = models.CharField(max_length=20) # 出题人
    last_edit = models.DateTimeField(auto_now_add=True)

    time_limit = models.IntegerField(default=1000) 
    mem_limit = models.IntegerField(default=64) # MB

    lang_allow = models.CharField(max_length=100, default="__all__")

    title = models.CharField(max_length = 20, default = "")
    cont_detial = models.CharField(max_length = 1000)
    cont_input = models.CharField(max_length = 1000)
    cont_output = models.CharField(max_length = 1000)
    cont_hint = models.CharField(max_length = 1000)
    source = models.CharField(max_length = 100)

    tags = models.CharField(max_length = 1000)

    spj = models.BooleanField(default=False)

    show_level = models.IntegerField(choices=to_choices(SHOW_MOD))

    tot_cnt = models.BigIntegerField(default=0)
    ac_cnt = models.BigIntegerField(default=0)
    wa_cnt = models.BigIntegerField(default=0)
    tle_cnt = models.BigIntegerField(default=0)
    mle_cnt = models.BigIntegerField(default=0)
    ce_cnt = models.BigIntegerField(default=0)
    se_cnt = models.BigIntegerField(default=0)
    re_cnt = models.BigIntegerField(default=0)
    me_cnt = models.BigIntegerField(default=0)