from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Blog(models.Model):
    # to be created
    pass


class Category(models.Model):
    name         = models.CharField(max_length=100)
    created_at   = models.DateTimeField(auto_now_add=True)
    modified_at  = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name        = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class NewPost(models.Model):
    COVER_POST_PIC_PATH   = "users/cover/blog/post/"
    
    DRAFT          = 'D'
    PUBLISHED      = 'P'
    STATUS_CHOICES = [
                        (DRAFT, 'Draft'),
                        (PUBLISHED, 'Published'),
    ]
    
    title        = models.CharField('Title', max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    cover_pic    = models.ImageField(upload_to=COVER_POST_PIC_PATH, verbose_name="main post image", null=True)
    new_category = models.ManyToManyField(Category, blank=True)
    blog         = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="posts")
    author       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    post         = CKEditor5Field('New post', config_name='extends', blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    modified_at  = models.DateTimeField(auto_now=True)
    is_live      = models.BooleanField(default=False)
    status       = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title