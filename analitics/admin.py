from django.contrib import admin

from .models import LikesActivity, UserLoginActivity


admin.site.register(LikesActivity)
admin.site.register(UserLoginActivity)
