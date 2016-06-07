class AutoSaveModelFormMixin(object):
    autosave_prefix = ''
    autosave_fields = []

    def __init__(self, *args, **kwargs):
        super(AutoSaveModelFormMixin, self).__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        if instance:
            instance_identifier = instance.id
        else:
            instance_identifier = 'add'

        for field_name in self.autosave_fields:
            field = self.fields[field_name]
            field.widget.attrs = field.widget.attrs or {}
            field.widget.attrs.update({
                'data-autosave': 'autosave_%s_%s:%s' % (self.autosave_prefix, instance_identifier, field),
            })

    @property
    def media(self):
        media = super(AutoSaveModelFormMixin, self).media
        media.add_js(['admin/js/admin-models-autosave.js'])
        return media
