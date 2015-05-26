# -*- coding: utf-8 -*-
from django.conf import settings

import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL
        strategy = factory.CREATE_STRATEGY

    full_name = factory.Sequence(lambda x: 'First{}'.format(x))
    email = factory.Sequence(lambda x: 'email{}@address.com'.format(x))
