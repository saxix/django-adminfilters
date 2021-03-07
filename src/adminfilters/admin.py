
class SmartFilterMixin:
    def __init__(self, model, admin_site):
        FieldListFilter.register(lambda f: bool(f.choices), ChoicesFieldComboFilter, True)
        FieldListFilter.register(lambda f: isinstance(f, models.BooleanField), AllValuesComboFilter, True)
        FieldListFilter.register(lambda f: f.remote_field, RelatedFieldComboFilter, True)

        super().__init__(model, admin_site)
