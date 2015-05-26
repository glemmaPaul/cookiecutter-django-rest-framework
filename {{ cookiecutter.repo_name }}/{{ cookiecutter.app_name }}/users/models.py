# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# Third party
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(blank=False, null=False, unique=True)
    full_name = models.CharField(max_length=255, blank=False, null=False)

    is_staff = models.BooleanField(_('Staff status'), default=False,
                                   help_text=_('Designates whether the user can'
                                               ' log into this admin site.'))

    is_active = models.BooleanField(_('Active'), default=True,
                                    help_text=_('Designates whether this user '
                                                'should be treated as '
                                                'active. Unselect this instead '
                                                'of deleting accounts.'))

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_short_name(self):
        return self.full_name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """ When a user is created create an authorization token for them """

    if created:
        Token.objects.create(user=instance)
