import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Название проекта
django.setup()  # Текущие настройки Django взяты выше, можно запускать.

from blog.models import Post, User
import requests

headers = {'Authorization': 'Token 93812749b34711bc5943ba2a14516e49f260bd99'}
url = 'http://127.0.0.1:8000/api'

response = requests.get(url, headers=headers)
print(response.json())
for i in response.json()['results']:
    print(i['id'])













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