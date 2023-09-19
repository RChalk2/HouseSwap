from django.contrib import admin
from .models import Kashrut, User, Property, Image

admin.site.register(User)
admin.site.register(Kashrut)
admin.site.register(Property)
admin.site.register(Image)
