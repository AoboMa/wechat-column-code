from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator,\
    UnicodeUsernameValidator
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from .backends import UserManager


# Create your models here.
class WechatUser(AbstractBaseUser, PermissionsMixin):
    '''
    微信用户model
    '''
    # 管理员账号验证规则
    systemid_validator = (UnicodeUsernameValidator() if six.PY3
                          else ASCIIUsernameValidator())

    # 字段
    openid = models.CharField(_("本公众号加密ID"), max_length=50, primary_key=True)
    unionid = models.CharField(_("多公众号共同ID"), max_length=50,
                               null=True, db_index=True)
    groupid = models.SmallIntegerField(_("用户所在用户组ID"), default=0)
    subscribe = models.BooleanField(_("关注"), default=True)
    subscribe_time = models.DateTimeField(_("关注时间"), auto_now_add=True)
    nickname = models.CharField(_("微信昵称"), max_length=100)
    sex = models.SmallIntegerField(_("性别:0未知,1男,2女"), default=0)
    language = models.CharField(_("语言"), max_length=100)
    city = models.CharField(_("城市"), max_length=100)
    province = models.CharField(_("省份"), max_length=100)
    country = models.CharField(_("国家"), max_length=100)
    remark = models.CharField(_("备注"), max_length=500, null=True)
    headimgurl = models.CharField(_("微信头像url"), max_length=300, null=True)
    systemid = models.CharField(
        _("管理员用户名"), max_length=50, null=True, unique=True,
        help_text=_('必填。50个或者更少的英文字符、数字或 @/./+/-/_'),
        validators=[systemid_validator],
        error_messages={'unique': _("您输入的用户名已经被占用")})
    password = models.CharField(_('管理员密码'), max_length=128, null=True)
    is_superuser = models.BooleanField(_("管理员"), default=False)
    created_time = models.DateTimeField(_("创建时间"), auto_now_add=True,
                                        db_index=True)
    updated_time = models.DateTimeField(_("更新时间"), auto_now=True)

    # models后台设定
    objects = UserManager()
    # 用户名字段设定为openid
    USERNAME_FIELD = 'openid'

    class Meta:
        verbose_name = _('微信用户')
        verbose_name_plural = _('微信用户')
