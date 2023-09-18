from django.contrib import admin
from .models import Kashrut, User, Property
admin.site.register(User)
admin.site.register(Kashrut)
admin.site.register(Property)

