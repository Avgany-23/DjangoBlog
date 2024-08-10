import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Название проекта

django.setup()  # Текущие настройки Django взяты выше, можно запускать.
from blog.models import Post, User

posts = Post.published.all()
for i in posts:
    print(i.id)
    print(i.tags.values_list('id', flat=True))
