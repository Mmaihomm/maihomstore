from django.db import models

# Create your models here.
class Catigories(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to= 'uploads/',max_length=200,default=None,null=True,blank=True)
    categoriesdetail = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to= 'uploads/',max_length=200,default=None,null=True,blank=True)
    productdetail = models.TextField(max_length=255)
    catigorie = models.CharField(max_length=100)
    price = models.CharField(max_length=5)
    recommend = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    image = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.product.name
    
