from os import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/market', views.index, name='index'),
    path('<str:sport_name>/', views.sport, name='sport_page'),
    path('<str:sport_name>/<int:game_id>', views.game, name='game_page'),
    path('<str:sport_name>/<int:game_id>/<int:comment_id>/reply', views.reply_comment, name='reply_comment'),
    path('<str:sport_name>/<int:game_id>/post_comment', views.post_comment, name='post_comment'),
]