from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import uuid

STATUS_CHOICES = (
    ('process', 'PROCESS'),
    ('shipping', 'SHIPPING'),
    ('done', 'DONE'),
)

class User(AbstractUser):
    name= models.CharField(max_length=200, null=True)
    email= models.EmailField(unique=True, null=True)
    phone= models.CharField(max_length=200, null=True)
    username= models.CharField(max_length=200, null=True, blank=True)

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username']
    #pass



class Catagory(models.Model):
    name=models.CharField(max_length=200)    
    image= models.ImageField(upload_to='catagory/')

    def __str__(self) -> str:
        return self.name


class FavouriteCatagory(models.Model):
    catagory= models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True)
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Product(models.Model):
    taitle= models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    catagory= models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True)
    price= models.CharField(max_length=200, null=True)
    WasPrice= models.CharField(max_length=200, null=True, blank=True) 
    DeleveryPrice= models.CharField(max_length=200, null=True)
    size=models.BooleanField(default=False)
    dicription= models.TextField()
    info= RichTextField(null=True)
    pub_date= models.DateTimeField(auto_now_add=True, null=True)

    def generate_unique_slug(self):
        slug = slugify(self.taitle)
        unique_slug = slug
        counter = 1
        while Product.objects.filter(slug=unique_slug).exclude(id=self.id).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.taitle

    @property
    def main_image(self):
        return self.productimage_set.first()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_main', 'created_at']

    def __str__(self):
        return f"Image for {self.product.taitle}"

    def save(self, *args, **kwargs):
        if self.is_main:
            # Set all other images of this product to not main
            ProductImage.objects.filter(product=self.product).update(is_main=False)
        # If this is the first image, make it the main image
        elif not ProductImage.objects.filter(product=self.product).exists():
            self.is_main = True
        super().save(*args, **kwargs)

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    size = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.host.username}'s cart - {self.product.taitle}"

class Wishlist(models.Model):
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    host= models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class CoverSell(models.Model): 
    image=models.ImageField(null=True,upload_to='coversell/')
    mobile_image=models.ImageField(null=True,upload_to='coversell/')
    url= models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return self.url

class CartOrder(models.Model):
    DELIVERY_CHOICES = (
        ('dhaka', 'Dhaka'),
        ('outside', 'Outside Dhaka'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    delivery_location = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='dhaka')
    home_address = models.CharField(max_length=500)
    town = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='process')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.name}"

    class Meta:
        ordering = ['-date']

class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=200, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.taitle} in Order #{self.order.id}"

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = float(self.product.price.replace('৳', '').replace('Tk', '').strip())
        super().save(*args, **kwargs)

class Order(models.Model):
    DELIVERY_CHOICES = (
        ('dhaka', 'Dhaka'),
        ('outside', 'Outside Dhaka'),
    )

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)        
    companyname = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200)
    delivery_location = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='dhaka')
    home_address = models.CharField(max_length=500)
    home_address2 = models.CharField(max_length=500, null=True, blank=True)
    town = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='process', null=True)
    quintity = models.CharField(max_length=200, null=True)
    size = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)



class Reveaws(models.Model):
    taitle= models.CharField(max_length=200, null=True)
    body= models.TextField()
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created= models.DateTimeField(auto_now_add=True, null=True)
    total= models.CharField(max_length=500,null=True)
    rating = models.IntegerField(null=True)

    class Meta:
        ordering= ['total']
            



class Subscriber(models.Model):
    email= models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.email



class FlashDeal(models.Model):
    image= models.ImageField(upload_to='flash/')
    taitle= models.CharField(max_length=200)
    price= models.CharField(max_length=200, null=True)
    url= models.CharField(max_length=200)
    background= models.ImageField(upload_to='flash/', null=True)


class TrendCover(models.Model):
    link= models.CharField(max_length=200, null=True)
    image= models.ImageField(upload_to='trend/')

# class Contact(models.Model):
#     phone= models.CharField(max_length=200, null=True)
#     email= models.EmailField(null=True)
#     address= models.CharField(max_length=500, null=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=200)
    home_address = models.CharField(max_length=500)
    home_address2 = models.CharField(max_length=500, blank=True)
    town = models.CharField(max_length=200)
    postcode = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user.username
    
class FeaturedProduct(models.Model):
    background= models.ImageField(upload_to='featured/', null=True)
    catagory= models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True)
    taitle= models.CharField(max_length=200)
    url= models.CharField(max_length=200)
    

    def __str__(self) -> str:
        return self.taitle

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Blog Categories"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = RichTextField()
    featured_image = models.ImageField(upload_to='blog/')
    excerpt = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.user.name} on {self.blog.title}'

    class Meta:
        ordering = ['-created_date']

class ProductReview(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True)
    title = models.CharField(max_length=200)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    images = models.ImageField(upload_to='reviews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return f"Review by {self.customer_name}"

class ReviewImage(models.Model):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.review.title}"