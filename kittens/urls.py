from django.urls import path
from . import apiviews


urlpatterns = [
    path(
        'kittens/<pk>/',
        apiviews.get_delete_update_kitten,
        name='get_delete_update_kitten'
    ),
    path(
        'kittens/',
        apiviews.get_post_kittens,
        name='get_post_kittens'
    )
]
