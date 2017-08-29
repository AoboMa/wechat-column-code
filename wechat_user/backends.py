'''
Created on 2017年8月29日

@author: maaobo
'''
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, openid, systemid, password, **extra_fields):
        """
        使用给出的openid, systemid和password创建一个用户
        """
        if not openid:
            raise ValueError('openid是主键，必须给定值，你可以在之后修改')
        if systemid:
            systemid = self.model.normalize_username(systemid)

        user = self.model(openid=openid, systemid=systemid, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, openid, systemid=None, password=None,
                    **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(openid, systemid, password, **extra_fields)

    def create_superuser(self, openid, systemid, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('创建管理员时is_superuser必须为True')

        return self._create_user(openid, systemid, password, **extra_fields)
