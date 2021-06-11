from django.contrib import admin
from .models import Catigories,Product,ProductImage

# Register your models here.

class CatigoriesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ['is_active']


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ['is_active',]
    inlines = [ProductImageAdmin]

    class Meta:
        model=Product

class ProductImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Catigories,CatigoriesAdmin)
admin.site.register(Product,ProductAdmin)