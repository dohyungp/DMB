from django.contrib import admin

from .models import Portfolio
from .models import Category

# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Category)