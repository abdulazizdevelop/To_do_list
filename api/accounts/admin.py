from django.contrib import admin

from api.accounts.models import User, UserConfirmationCode

admin.site.register(User)
admin.site.register(UserConfirmationCode)

