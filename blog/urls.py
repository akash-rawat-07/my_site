from django.urls import path
from . import views


# For-Class Based urls
urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(), name="post-detail-page"),
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]


# For-Function Based urls
# urlpatterns = [
    # path("", views.starting_page, name="starting-page"),
    # path("posts", views.posts, name="posts-page"),
    # path("posts/<slug:slug>", views.post_detail, name="post-detail-page"),
# ]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)