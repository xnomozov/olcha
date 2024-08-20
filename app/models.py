from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True, editable=False, blank=True, null=False)
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Group(TimestampedModel):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True, editable=False, blank=True, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='groups')
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Group.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimestampedModel):
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.FloatField()
    slug = models.SlugField(max_length=300, unique=True, editable=False, blank=True, null=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    discount = models.FloatField(default=0)
    user_like = models.ManyToManyField(User)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super(Product, self).save(*args, **kwargs)

    @property
    def discounted_price(self):
        if self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    def get_attribute(self):
        product_attribute = ProductAttribute.objects.filter(product=self)
        attributes = []
        for prod_at in product_attribute:
            attributes.append({
                'attribute_key': prod_at.key,
                'attribute_value': prod_at.value
            })
        return attributes

    @property
    def get_attributes_as_dict(self) -> dict:
        attributes = self.get_attribute()
        attributes_dict = {}
        for attribute in attributes:
            attributes_dict[attribute['attribute_key']] = attribute['attribute_value']

        return attributes_dict

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)


class Comment(TimestampedModel):
    class Rating(models.IntegerChoices):
        zero = 0
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5

    rating = models.IntegerField(choices=Rating.choices, default=Rating.zero.value)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

    def save(self, *args, **kwargs):
        if not self.user:
            request = kwargs.get('request')
            user = request.user
            self.user = user

        super(Comment, self).save(*args, **kwargs)

class AttributeKey(models.Model):
    key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.key


class AttributeValue(models.Model):
    value = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.value


class ProductAttribute(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE, related_name='attributes')
    key = models.ForeignKey('app.AttributeKey', on_delete=models.CASCADE)
    value = models.ForeignKey('app.AttributeValue', on_delete=models.CASCADE)
