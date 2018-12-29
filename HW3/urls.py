"""HW3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include
from django.urls import path
from Twitter import views
from HW3 import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  url(r'^$', views.index, name='index'),
                  path('logout/', views.signout, name='signout'),
                  url(r'^auth/', include('social_django.urls', namespace='social')),
                  path('edit/', views.edit_profile, name='edit'),
                  path('feed/', views.feed, name='feed'),
                  path('<str:username>/', views.profile, name='profile'),
                  path('<str:username>/following/', views.follows, name='follows'),
                  path('<str:username>/followers/', views.followers, name='following'),
                  path('<str:username>/follow/', views.follow, name='follow'),
                  path('<str:username>/stopfollow/', views.stopfollow, name='stopfollow'),
                  path('<str:username>/get_token_v2/', views.get_token_v2, name='get_token_v2'),
                  path('api/v2/tweet', views.tweet_by_token, name='tweet_by_token'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
