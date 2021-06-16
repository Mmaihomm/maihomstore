from django.db import models

# Create your models here.
class Catigories(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to= 'uploads/',max_length=200,default=None,null=True,blank=True)
    categoriesdetail = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return '%s' % self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to= 'uploads/',max_length=200,default=None,null=True,blank=True)
    productdetail = models.TextField(max_length=255)
    catigorie = models.ForeignKey(Catigories,default=None,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=2, help_text='price', default=0)
    recommend = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    image = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.product.name
    
class Contact(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.firstname


