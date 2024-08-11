from django import forms
from blog.models import Comment

class EmailPostForm(forms.Form):
    """
    Форма для функции 'поделиться статьёй'.
    Используется в detail.html.
    """

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """
    Класс формы для отправки комментариев.
    Имеет связь с моделью Comment.
    Используется в detail.html.
    """

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    """Класс-форма для полнотекстового поиска статей"""

    query = forms.CharField()
