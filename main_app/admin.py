from django.contrib import admin
# add Feeding to the import
from .models import Home, Amenity, Photo

admin.site.register(Home)

admin.site.register(Amenity)

admin.site.register(Photo)
