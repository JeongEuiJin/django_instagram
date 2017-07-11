from django.conf.urls import include,url

from post.urls import urls_apis as post_urls

urlpatterns = [
    url(r'^post/', include('post.urls.urls_apis'))
]