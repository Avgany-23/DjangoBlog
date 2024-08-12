import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Название проекта
django.setup()  # Текущие настройки Django взяты выше, можно запускать.

from blog.models import Post, User
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity

# posts = 'Django'
# search_vector = SearchVector('title', 'body')
# search_query = SearchQuery(posts)
#
# query = 'django'
# results = Post.published.annotate(
#     similarity=TrigramSimilarity('title', query),
# ).filter(similarity__gt=0.1).order_by('-similarity')
# res = TrigramSimilarity('title', query)
# print(res)

# print(search_query)
# for i in posts:
#     # print(i.id)
#     print(i.tags.values_list('id', flat=True))








# from django.contrib.auth.models import User


# user = User.objects.create_user(username='user_two',
#                                  email='user_one1@google.com',
#                                  password='user07112')
# user = User.objects.get(username='user_two')
# print(user.is_anonymous)

















# path('', views.PostListView.as_view(), name='post_list'),
# from django.views.generic import ListView
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