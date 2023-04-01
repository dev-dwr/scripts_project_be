from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.get_all_offers, name='offers'),
    path('offers/', views.create_new_offer, name='offer_newly_created'),
    path('offers/<str:pk>', views.get_offer_by_pk, name='offer_by_pk'),
    path('offers/<str:pk>/update', views.update_existing_offer_by_pk, name='offer_update'),
    path('offers/<str:pk>/delete', views.delete_offer_by_pk, name='offer_delete'),
    path('offers/<str:pk>/apply', views.apply_for_the_offer, name='apply_offer'),
    path('offers/statistics/<str:title>', views.get_offer_statistics, name='offer_statistics')
]