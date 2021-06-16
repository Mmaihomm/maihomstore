from django.contrib import admin
from .models import Catigories,Product,ProductImage,Contact

# Register your models here.

class CatigoriesAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['name','categoriesdetail','is_active']
    list_filter = ['is_active']


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ['name','productdetail','catigorie','price','recommend','is_active','image']
    list_filter = ['is_active','catigorie']
    inlines = [ProductImageAdmin]

    class Meta:
        model=Product

class ProductImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Catigories,CatigoriesAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Contact)
admin.site.register(ProductImage,ProductImageAdmin)