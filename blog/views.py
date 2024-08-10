from django.db.models import Count
from .models import Post
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from taggit.models import Tag


@require_POST
def post_comment(request, post_id: int) -> render:
    """Функция реагирует только на POST запросы
    Обрабатывает информацию с формы CommentForm и создаёт комментарий
    под постом с id = post_id"""

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)   # Комментарий был отправлен
    if form.is_valid():
        comment = form.save(commit=False)   # Создать объект класса Comment, не сохраняя его в базе данных
        comment.post = post                 # Назначить пост комментарию
        comment.save()                      # Сохранить комментарий в базе данных
    return render(request, 'blog/post/comment.html',
                  {'post': post, 'form': form, 'comment': comment})


def post_detail(request, year: int, month: int, day: int, post: int) -> render:
    """Функция отображает полную информацию о статье"""

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)    # Список активных комментариев к этому посту
    form = CommentForm()                            # Форма для комментирования пользователями

    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                                          'comments': comments,
                                                                          'form': form,
                                                                          'similar_posts': similar_posts})


def post_share(request, post_id: int) -> render:
    """
    GET-request: отображает форму EmailPostForm
    POST-request: проверяет заполненные данные EmailPostForm на валидность
    """
    sent = True
    post = Post.published.get(id=post_id)

    if request.method == 'POST':
        email_form = EmailPostForm(request.POST)
        if email_form.is_valid():
            data = email_form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{data['name']} recommends you read " \
                      f"{post.title}"

            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{data['name']}\'s ({data['email']}) comments: {data['comments']}"

            send_mail(subject, message, settings.EMAIL_HOST_USER,[data['to']])

    else:
        sent = False
        email_form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'form': email_form,
                                                                         'sent': sent,
                                                                         'post': post})


# class MyPaginator(Paginator):
#     def validate_number(self, number):
#         try:
#             return super().validate_number(number)
#         except EmptyPage:
#             if int(number) > 1:
#                 return self.num_pages
#             elif int(number) < 1:
#                 return 1
#             else:
#                 raise


# class PostListView(ListView):
#     """Альтернативное представление списка постов"""
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'
#     paginator_class = MyPaginator


def post_list(request, tag_slug: str | None = None) -> render:
    """Функция отображает список опубликованных постов.
    Если tag_slug is not None, то отображается список постов с тегом = tag_slug"""
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:                         # Есди page_number не целое число, то первая страница
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # Если page_number вне диапазона, то последняя страницы

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag})