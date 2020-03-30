from django.contrib import admin

# Register your models here.


from .models import Location

admin.site.register(Location)

from .models import Asset

admin.site.register(Asset)

from .models import Service

admin.site.register(Service)