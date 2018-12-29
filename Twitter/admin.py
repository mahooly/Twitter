from django.contrib import admin
from Twitter.models import *

admin.site.register(Profile)
admin.site.register(RequestData)
admin.site.register(Tweet)
admin.site.register(Follow)
admin.site.register(LoggedInUser)
