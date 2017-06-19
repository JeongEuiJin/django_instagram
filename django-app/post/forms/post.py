from django import forms
from ..models import Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True

    comment = forms.CharField(
        required=False,
        widget=forms.TextInput
    )

    class Meta:
        model = Post
        fields = (
            'photo',
            'comment',
        )

    def save(self, **kwargs):
        commit = kwargs.get('commit', True)
        author = kwargs.pop('author', None)

        self.instance.author = author
        instance = super().save(**kwargs)

        comment_string = self.cleaned_data['comment']
        if commit and comment_string:
            instance.comment_set.create(
                author=instance.author,
                content=self.comment
            )
        return instance
