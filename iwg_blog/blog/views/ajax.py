from django.db import models
from django.http import JsonResponse
from django.views.generic import View

from ..models import Article, Tag


class GetArticleSlugAjax(View):
    def post(self, *args, **kwargs):
        return JsonResponse({
            'status': 'ok',
            'slug': Article.generate_slug(
                self.request.POST.get('title', ''),
                instance_pk=self.request.POST.get('instance_pk')
            )
        })


class TagsAutocompleteAjax(View):
    tags_count = 10

    def get(self, request, *args, **kwargs):
        tag = request.GET.get('term', '')
        exclude = request.GET.getlist('exclude')

        queryset = Tag.objects.filter(name__startswith=tag).exclude(name__in=exclude) \
            .annotate(article_count=models.Count('articles')).order_by('-article_count') \
            .values_list('name', flat=True)[:self.tags_count]

        return JsonResponse(list(queryset), safe=False)
