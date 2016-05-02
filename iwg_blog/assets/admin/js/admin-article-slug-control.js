$(document).ready(function(){
    var $slug = $('input[name="slug"]');
    var $title = $('input[name="title"]');
    var $help_text = $slug.parent().find('.grp-help');
    var help_text_template = "link to new article would be: ";

    if ($slug.length == 0 || $title.length == 0){
        return true;
    }

    function updateSlug(){
        var ajax_data = {'title': $title.val()};
        if (populate_slug_opts.instance_pk){
            ajax_data['instance_pk'] = populate_slug_opts.instance_pk;
        }
        $.post(populate_slug_opts.ajax_url, ajax_data, function(data){
            $slug.val(data['slug']);
            updateHelpText();
        })
    }

    function updateHelpText(){
        $help_text.html(help_text_template + populate_slug_opts.template_url.replace('dummy_slug', $slug.val()));
    }
    
    updateHelpText();
    $title.on('keyup', updateSlug);
    $slug.on('keyup change', updateHelpText);
});