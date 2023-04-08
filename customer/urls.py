from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_new_user, name='register_new_user'),
    path('current_user', views.get_current_user, name='get_current_user'),
    path('current_user/update', views.update_existing_user_credentials, name='update_existing_user'),
    path('current_user/cv', views.upload_user_cv, name='upload_user_cv'),
]