from django.contrib.admin.templatetags import admin_modify


@admin_modify.register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    """
    Overriding default submit row admin template tag to use some additional actions from context.
    """
    tag_context = admin_modify.submit_row(context)
    tag_context.update({
        'additional_actions': context.get('additional_actions', [])
    })
    return tag_context
