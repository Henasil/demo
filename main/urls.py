from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('application/create/', views.create_application_view, name='create_application'),
    path('review/<int:application_id>/', views.review_view, name='review'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]
