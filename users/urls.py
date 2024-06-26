from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [ 
    path('login/', login_api,name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('info/', UserInfoView.as_view(), name='info'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]