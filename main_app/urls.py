from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('homes/', views.homes_index, name='index'),
    path('homes/<int:home_id>/', views.homes_detail, name='detail'),
    path('homes/create', views.HomeCreate.as_view(), name='homes_create'),
    path('homes/<int:pk>/update/', views.HomeUpdate.as_view(), name='homes_update'),
    path('homes/<int:pk>/delete/', views.HomeDelete.as_view(), name='homes_delete'),
    path('homes/<int:home_id>/add_photo/', views.add_photo, name='add_photo'),
    path('homes/<int:home_id>/assoc_amenity/<int:amenity_id>/',
         views.assoc_amenity, name='assoc_amenity'),
    path('amenities/', views.AmenityList.as_view(), name='amenities_index'),
    path('amenitites/<int:pk>/', views.AmenityDetail.as_view(), name='amenities_detail'),
    path('amenities/create/', views.AmenityCreate.as_view(),
         name='amenities_create'),
    path('amenities/<int:pk>/update/',
         views.AmenityUpdate.as_view(), name='amenities_update'),
    path('amenities/<int:pk>/delete/',
         views.AmenityDelete.as_view(), name='amenities_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]
