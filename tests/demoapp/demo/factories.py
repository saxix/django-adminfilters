import random

import factory
import factory.fuzzy
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from factory.base import FactoryMetaClass

from . import models

factories_registry = {}


class AutoRegisterFactoryMetaClass(FactoryMetaClass):
    def __new__(mcs, class_name, bases, attrs):
        new_class = super().__new__(mcs, class_name, bases, attrs)
        factories_registry[new_class._meta.model] = new_class
        return new_class


class ModelFactory(factory.django.DjangoModelFactory, metaclass=AutoRegisterFactoryMetaClass):
    pass


class DemoRelatedFactory(ModelFactory):
    class Meta:
        model = models.DemoRelated


class DemoModelFactory(ModelFactory):
    name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    demo_related = factory.SubFactory(DemoRelatedFactory)

    class Meta:
        model = models.DemoModel

    @factory.lazy_attribute
    def flags(self):
        # Convert to plain ascii text
        f = lambda: random.choice([
            ("int", random.randint(1, 100)),
            ("chr", chr(random.randrange(65, 90))),
            ("int", '__'),
            ("chr", ""),
            ("chr", None),
            ("int", None),
            ("chr", '__'),
        ])
        value = f()
        if value[1] == '__':
            base = {}
        else:
            base = dict([value])
        value = f()
        if value[1] != '__':
            base.update(dict([value]))
        return base


def get_factory_for_model(_model):
    class Meta:
        model = _model

    if _model in factories_registry:
        return factories_registry[_model]
    return type("AAA", (ModelFactory,), {'Meta': Meta})
