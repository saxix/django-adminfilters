import random

import factory.fuzzy
import faker
from django.contrib.auth.models import User
from factory.base import FactoryMetaClass

from . import models

factories_registry = {}


class AutoRegisterFactoryMetaClass(FactoryMetaClass):
    def __new__(mcs, class_name, bases, attrs):
        new_class = super().__new__(mcs, class_name, bases, attrs)
        factories_registry[new_class._meta.model] = new_class
        return new_class


class ModelFactory(
    factory.django.DjangoModelFactory, metaclass=AutoRegisterFactoryMetaClass
):
    pass


def get_flags():
    # Convert to plain ascii text
    f = lambda: random.choice(
        [
            ("int", random.randint(1, 100)),
            ("chr", chr(random.randrange(65, 90))),
            ("int", "__"),
            ("chr", ""),
            ("chr", None),
            ("int", None),
            ("chr", "__"),
        ]
    )
    value = f()
    if value[1] == "__":
        base = {}
    else:
        base = dict([value])
    value = f()
    if value[1] != "__":
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
    json = {"char": "string", "integer": 100, "float": 2.0}

    class Meta:
        model = models.DemoModelField

    @factory.lazy_attribute
    def flags(self):
        return get_flags()


class UserFactory(ModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)


class CountryFactory(ModelFactory):
    name = factory.Faker("country")

    class Meta:
        model = models.Country
        django_get_or_create = ("name",)


class BandFactory(ModelFactory):
    name = factory.Faker("name")
    genre = factory.fuzzy.FuzzyChoice([1, 2, 3, 4])

    class Meta:
        model = models.Band
        django_get_or_create = ("name",)


class ArtistFactory(ModelFactory):
    name = factory.Faker("first_name")
    last_name = factory.Sequence(lambda n: f'Dummy{faker.Faker().unique.last_name()}{n}')
    full_name = factory.LazyAttribute(lambda o: f"{o.last_name}, {o.name}")

    country = factory.SubFactory(CountryFactory)
    year_of_birth = factory.Faker("year")

    class Meta:
        model = models.Artist
        django_get_or_create = ("name", "last_name")

    @factory.post_generation
    def bands(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted is None:
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
    return type("AAA", (ModelFactory,), {"Meta": Meta})
