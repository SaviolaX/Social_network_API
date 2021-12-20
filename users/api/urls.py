from django.urls import path

from .api_view import (RegisterView, LoginView, UserView,
                       LogoutView, UserByIdView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),

    path('user/', UserView.as_view(), name='user_view'),
    path('user/<int:id>/', UserByIdView.as_view(), name='user_view_by_id'),
]
