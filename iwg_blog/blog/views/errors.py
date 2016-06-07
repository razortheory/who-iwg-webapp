from django.shortcuts import render

from ..models import Article


def page_not_found(request):
    return render(
        request, 'blog/pages/404.html',
        {
            'related_articles': Article.published.all()[:3]
        }, status=404
    )


def server_error(request):
    return render(request, 'blog/pages/500.html', status=500)
