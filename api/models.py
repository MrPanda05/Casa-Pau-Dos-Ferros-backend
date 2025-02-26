from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

class User(AbstractUser):
    full_name = models.CharField(max_length=150, unique=False, default='User');
    birth_date = models.DateField(default=timezone.now);
    cpf = models.CharField(max_length=11, null=False, default='00000000000');
    
    def __str__(self):
        return self.username

class user_address(models.Model):
    address_id = models.AutoField(primary_key=True)
    cep = models.CharField(max_length=8, null=False)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=80)
    number = models.CharField(max_length=8)
    complement = models.CharField(max_length=80, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, models.CASCADE, db_column='user_id', null=True, default=0)

    def __str__(self):
        return str(self.address_id)

def get_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'{instance.product_id}.{ext}'
    return 'media/product' + '/' + new_filename

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    reserved = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    image = models.ImageField(upload_to='media/product', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
@receiver(post_save, sender=Product)
def rename_image_filename(sender, instance, created, **kwargs):
    if instance.image:
        # Rename file after the product is saved and pk is set
        new_filename = get_upload_to(instance, instance.image.name)
        # Move the file to the new location
        if instance.image.name != new_filename:
            os.rename(instance.image.path, new_filename)
            # If file name has changed, save with the new name
            instance.image.name = new_filename
            instance.save()  # Trigger re-save with new filename

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, models.CASCADE, db_column='category_id', default=1)
    product = models.ForeignKey(Product, models.CASCADE, db_column='product_id', default=1)

    class Meta:
        unique_together = ('category', 'product')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):

    class Status(models.IntegerChoices):
        Open = 0
        Confirmed = 1
        Canceled = 2
    
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, models.CASCADE, db_column='user_id', default=1)
    is_active = models.BooleanField(default=True)
    status = models.IntegerField(choices=Status.choices, default=Status.Open)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cart_id)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, models.CASCADE, db_column='cart_id')
    product = models.ForeignKey(Product, models.CASCADE, db_column='product_id')
    quantity = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')


    def __str__(self):
        return str(self.product.product_id)
    
# class Order(models.Model):
#     class Status(models.IntegerChoices):
#         Pending = 0
#         Finished = 1
#         Canceled = 2

#     order_id = models.AutoField(primary_key=True)
#     cart = models.ForeignKey(Cart, models.CASCADE, db_column='cart_id')
#     user_address = models.ForeignKey(user_address, models.CASCADE, db_column='address_id')
#     status = models.IntegerField(choices=Status.choices, default=Status.Pending)
#     total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class OrderItem(models.Model):
#     order_id = models.ForeignKey(Order, models.CASCADE, db_column='order_id')
#     cart_item = models.ForeignKey(CartItem, models.CASCADE, db_column='cart_item_id')
#     total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)