from django.conf.urls import url
from . import views
from blog.views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    url(r'^$', PostList.as_view(), name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', PostDetail.as_view(), name='post_detail'),
    url(r'^post/new/$', PostCreate.as_view(), name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', PostUpdate.as_view(),
        name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', PostDelete.as_view(),
        name='post_remove'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$',
        views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/comment/$',
        views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$',
        views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$',
        views.comment_remove, name='comment_remove'),
    url(r'^user/new/$', views.user_new, name='user_new'),
    url(r'^access_denied/$', views.access_denied, name='access_denied'),
]
