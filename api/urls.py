from django.urls import re_path

from api import views

urlpatterns = [
    re_path(r'^management/recreate-index/?$', views.management.recreate_index),
    re_path(r'^management/learn-categories/?$', views.management.learn_categories),

    re_path(r'^statistics/stor(?:ag)?e/?$', views.statistics.storage),

    re_path(r'^documents/count/?$', views.documents.count),
    re_path(r'^documents/upload/?$', views.documents.upload),
    re_path(r'^documents/search/?$', views.documents.search),
    re_path(r'^documents/scan/?$', views.documents.scan),
    re_path(r'^documents/recent(/(?P<order>[a-z]+)(/(?P<offset>\d+)/(?P<limit>\d+))?)?/?$', views.documents.recent),

    re_path(r'^documents/(?P<path>[a-z0-9-]+)/?$', views.documents.index),
    re_path(r'^documents/(?P<path>[a-z0-9-]+)/preview/?$', views.documents.download),
    re_path(r'^documents/(?P<path>[a-z0-9-]+)/download/?$', views.documents.download),
    re_path(r'^documents/(?P<path>[a-z0-9-]+)/confirm/?$', views.documents.confirm),

    re_path(r'^categories/?$', views.categories.categories),
    re_path(r'^categories/count/?$', views.categories.count),
    re_path(r'^categories/(?P<name>\w{1,20})/?$', views.categories.category),
    re_path(r'^categories/(?P<name>\w{1,20})/assign/?$', views.categories.assign),
    re_path(r'^categories/(?P<name>\w{1,20})/documents(/(?P<offset>\d+)/(?P<limit>\d+))?/?$', views.categories.documents),
]
