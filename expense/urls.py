from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('', views.home, name="home"),
    path('add-expense/', views.add_expense, name="add-expense"),
    path('update-expense/<str:pk>/', views.update_expense, name="update-expense"),
    path('delete-expense/<str:pk>/', views.delete_expense, name="delete-expense"),
]
