from django.urls import path

from .api_view import (LikesActivityList,
                       LikesActivityRangeFilter, UserLoginLogs)

urlpatterns = [
    path('analitics/', LikesActivityList.as_view(), name='likes_list'),
    path('analitics/date_from/<int:from_year>-<int:from_month>-<int:from_day>/date_to/<int:to_year>-<int:to_month>-<int:to_day>/',
         LikesActivityRangeFilter.as_view(), name='likes_filter_range'),

    path('analitics/user/<int:id>/logs/',
         UserLoginLogs.as_view(), name='user_log'),
]
