from django.contrib import admin
from six import string_types


class ConfigurableModelAdmin(admin.ModelAdmin):
    def _filter_configurable_list(self, request, configurable_list, prefix):
        for filter_attr in configurable_list:
            filter_func_name = prefix + filter_attr
            if hasattr(self, filter_func_name) and not getattr(self, filter_func_name)(request):
                configurable_list.remove(filter_attr)
        return configurable_list

    def get_list_filter(self, request):
        list_filter = super(ConfigurableModelAdmin, self).get_list_filter(request)[:]
        return self._filter_configurable_list(request, list_filter, 'list_filter_')

    def get_list_display(self, request):
        list_display = super(ConfigurableModelAdmin, self).get_list_display(request)[:]
        return self._filter_configurable_list(request, list_display, 'list_display_')


def remove_from_fieldsets(fieldsets, fields):
    if isinstance(fields, string_types):
        fields = [fields, ]

    for fieldset in fieldsets:
        for field in fields:
            if field in fieldset[1]['fields']:
                newfields = []
                for myfield in fieldset[1]['fields']:
                    if not myfield in fields:
                        newfields.append(myfield)

                fieldset[1]['fields'] = tuple(newfields)
                break
