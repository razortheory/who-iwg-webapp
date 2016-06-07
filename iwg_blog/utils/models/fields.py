from django.db import models

from autoslug import AutoSlugField as RealAutoSlugField


class OrderedManyToManyField(models.ManyToManyField):
    """Model field; Keeping related objects ordering at saving"""
    def save_form_data(self, instance, data):
        m2m_model = getattr(instance, self.attname).through
        m2m_model.objects.filter(**{self.m2m_field_name(): instance}).delete()
        objects_to_create = [
            m2m_model(**{
                self.m2m_field_name(): instance,
                self.m2m_reverse_field_name(): related_instance
            }) for related_instance in data
        ]
        m2m_model.objects.bulk_create(objects_to_create)


class AutoSlugField(RealAutoSlugField):
    # Work around https://bitbucket.org/neithere/django-autoslug/issues/34/django-migrations-fail-if-autoslugfield
    def deconstruct(self):
        name, path, args, kwargs = super(AutoSlugField, self).deconstruct()
        if 'manager' in kwargs:
            del kwargs['manager']
        return name, path, args, kwargs
