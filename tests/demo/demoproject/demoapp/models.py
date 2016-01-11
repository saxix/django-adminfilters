from django.db import models


class DemoModelField(models.Model):
    char = models.CharField(max_length=255)
    integer = models.IntegerField()
    logic = models.BooleanField(default=False)
    null_logic = models.NullBooleanField(default=None)
    date = models.DateField()
    datetime = models.DateTimeField()
    time = models.TimeField()
    decimal = models.DecimalField(max_digits=10, decimal_places=3)
    email = models.EmailField()
    #    filepath = models.FilePathField(path=__file__)
    float = models.FloatField()
    bigint = models.BigIntegerField()
    generic_ip = models.GenericIPAddressField()
    url = models.URLField()
    text = models.TextField()

    unique = models.CharField(max_length=255, unique=True)
    nullable = models.CharField(max_length=255, null=True)
    blank = models.CharField(max_length=255, blank=True, null=True)
    not_editable = models.CharField(max_length=255, editable=False,
                                    blank=True, null=True)
    choices = models.IntegerField(choices=((1, 'Choice 1'),
                                           (2, 'Choice 2'),
                                           (3, 'Choice 3')))

    class Meta:
        app_label = 'demoapp'


class DemoRelated(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class DemoModel(models.Model):
    name = models.CharField(max_length=255)
    demo_related = models.ForeignKey('DemoRelated')

    class Meta:
        app_label = 'demoapp'


class DemoModel_RelatedFieldCheckBoxFilter(DemoModel):

    class Meta:
        proxy = True
        verbose_name = "RelatedFieldCheckBoxFilter"


class DemoModel_RelatedFieldRadioFilter(DemoModel):

    class Meta:
        proxy = True
        verbose_name = "RelatedFieldRadioFilter"


class DemoModel_UnionFieldListFilter(DemoModel):

    class Meta:
        proxy = True
        verbose_name = "UnionFieldListFilter"


class DemoModel_IntersectionFieldListFilter(DemoModel):

    class Meta:
        proxy = True
        verbose_name = "IntersectionFieldListFilter"
