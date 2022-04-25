"""SportsPrediction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path, re_path
from django.shortcuts import render, redirect
from web3auth import views as webviews
from market import views as marketviews
from django.views.generic import RedirectView
from .views import *

from django.conf import settings
from django.conf.urls.static import static

def login(request):
    render(request, 'web3auth/login.html')
    # if not request.user.is_authenticated:
    #     return render(request, 'web3auth/login.html')
    # else:
    #     return redirect('/admin/login')


def auto_login(request):
    if not request.user.is_authenticated:
        return render(request, 'web3auth/autologin.html')
    else:
        return redirect('/admin/login')

urlpatterns = [
    path('market/', include('market.urls'), name='home'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('trade_success/', marketviews.trade_success, name='trade_success'),
    path('redeem_success/', marketviews.redeem_success, name='trade_success'),
    path('before_buy_complete/', marketviews.before_buy_complete, name='before_buy_complete'),
    path('before_sell_complete/', marketviews.before_sell_complete, name='before_sell_complete'),

    path('like_comment/<int:game_id>/<int:comment_id>', marketviews.like_comment, name='like_comment'),
    path('dislike_comment/<int:game_id>/<int:comment_id>', marketviews.dislike_comment, name='dislike_comment'),
    path('cancel_like_comment/<int:game_id>/<int:comment_id>', marketviews.cancel_like_comment, name='cancel_like_comment'),
    path('cancel_dislike_comment/<int:game_id>/<int:comment_id>', marketviews.cancel_dislike_comment, name='cancel_dislike_comment'),

    path('save_trade/', marketviews.save_trade, name='save_trade'),
    re_path(r'^admin/', admin.site.urls),
    path('', index, name='columbia_home'), 
    path('user_logout/', marketviews.logout_view, name='user_logout'),
    re_path(r'^login_api/$', webviews.login_api, name='web3auth_login_api'),
    re_path(r'^signup_api/$', webviews.signup_api, name='web3auth_signup_api'),
    re_path(r'^signup/$', webviews.signup_view, name='web3auth_signup'),
    re_path(r'^auto_login/', auto_login, name='autologin'),
]
