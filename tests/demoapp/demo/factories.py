import random

import factory.fuzzy
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


def get_flags():
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


class DemoModelFieldFactory(ModelFactory):
    char = factory.Faker("name")
    integer = factory.Faker("pyint")
    date = factory.Faker("date_this_decade")
    datetime = factory.Faker("date_this_decade")
    time = factory.Faker("time")
    logic = factory.Faker("pybool")
    decimal = factory.Faker("coordinate")
    float = factory.Faker("pyfloat")
    bigint = factory.Faker("pyint")
    generic_ip = factory.Faker("ipv4")
    choices = factory.fuzzy.FuzzyChoice([1, 2, 3])
    unique = factory.Sequence(lambda a: a)
    email = factory.Faker("email")

    class Meta:
        model = models.DemoModelField

    @factory.lazy_attribute
    def flags(self):
        return get_flags()


class CountryFactory(ModelFactory):
    name = factory.Faker('country')

    class Meta:
        model = models.Country
        django_get_or_create = ('name',)


class BandFactory(ModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = models.Band
        django_get_or_create = ('name',)


class ArtistFactory(ModelFactory):
    name = factory.Faker('name')
    last_name = factory.Faker('last_name')
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = models.Artist

    @factory.post_generation
    def bands(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if not extracted:
            # A list of groups were passed in, use them
            extracted = [BandFactory()]
        for topping in extracted:
            self.bands.add(topping)

    @factory.lazy_attribute
    def flags(self):
        return get_flags()


def get_factory_for_model(_model):
    class Meta:
        model = _model

    if _model in factories_registry:
        return factories_registry[_model]
    return type("AAA", (ModelFactory,), {'Meta': Meta})
