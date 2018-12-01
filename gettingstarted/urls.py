from django.urls import path, re_path, include

from django.contrib import admin

admin.autodiscover()

# import bot.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

from bot.views import CommandReceiveView

urlpatterns = [
    # path("", hello.views.index, name="index"),
    # path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    re_path(r"^bot/(?P<bot_token>.+)/$", CommandReceiveView.as_view(), name="command"),
]
