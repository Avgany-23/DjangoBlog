from django import template
from ..models import Post
from django.db.models import Count


register = template.Library()


@register.simple_tag
def total_posts():
    """
    Функция возвращает количество опубликованных статей - int
    Обращение в HTML: {% total_posts %}
    """

    return Post.published.count()


@register.simple_tag
def none_nublished_post():
    """
    Функция возвращает количество НЕ опубликованных статей - int
    Обращение в HTML: {% none_nublished_post %}
    """

    return Post.objects.filter(status='DF').count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    Функция возвращает HTML шаблон с count самых последних опубликованных статей
    Обращение в HTML: {% show_latest_posts 3 %}
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """
    Функция возвращает count постов, имеющих наибольшее количество комментариев
    """
    return (Post.published.annotate(total_comments=Count('comments')).
                                                   exclude(total_comments=0).
                                                   order_by('-total_comments')[:count])