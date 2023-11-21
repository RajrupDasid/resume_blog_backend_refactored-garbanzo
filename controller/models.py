from django.db import models
import random
import string
import uuid
from django.utils.crypto import get_random_string
from django.template.defaultfilters import slugify
from django.conf import settings
import os
from io import BytesIO
from PIL import Image as Img
from django.core.files.uploadedfile import InMemoryUploadedFile
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from taggit.managers import TaggableManager
from analytics.models import Analytics
# Create your models here.


def random_uuid():
    random_uuid = uuid.uuid4()
    return str(random_uuid)


def random_string_generator(size=43, char=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def random_id_generator(size=15, char=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def thumbnail_upload_location(instance, filename):
    random_chars = get_random_string(22)
    image_file = random_chars
    random_image_name = get_random_string(27)
    _, file_extension = os.path.splitext(filename)
    image_name = f"{random_image_name}{file_extension}"
    return os.path.join(random_uuid(), image_file, image_name)


def media_file_upload(instance, filename):
    file_description = random_string_generator()
    random_file_name = get_random_string(33)
    _, file_extension = os.path.splitext(filename)
    file_name = f"{random_file_name}{file_extension}"
    return os.path.join(random_uuid(), file_description, random_file_name, file_name)


def normalize_catrgory(category):
    return slugify(category)


class Blog(models.Model):
    _id = models.CharField(default=random_string_generator,
                           blank=False, null=False, auto_created=True, max_length=900)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_location, null=True, blank=True, default=None)
    files = models.FileField(upload_to=media_file_upload,
                             null=True, blank=True, default=None, max_length=355)
    category = models.CharField(
        max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=500, unique=True)
    tags = TaggableManager(blank=True)
    content = RichTextUploadingField(default=None, blank=True, null=True)
    analytics = models.ForeignKey(
        Analytics, on_delete=models.CASCADE, related_name="analytics", blank=True, null=True, default=None)
    featured = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Blog has been generate with id {self._id} | with title {self.title} | at {self.created}"

    def save(self, *args, **kwargs):
        if self.thumbnail and self.thumbnail != self._get_old_thumbnail():
            img = Img.open(BytesIO(self.thumbnail.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            if img.mode != 'RGBA' and img.format == 'PNG':
                img = img.convert('RGBA')
            img.thumbnail((self.thumbnail.width / 1.5,
                          self.thumbnail.height / 1.5), Img.BOX)
            output = BytesIO()
            img.save(output, format='WebP', quality=80)
            output.seek(0)
            self.thumbnail = InMemoryUploadedFile(output, 'ImageField', "%s.webp" % self.thumbnail.name.join(
                random_string_generator()).split('.')[0:10], 'thumbnail/webp', len(output.getbuffer()), None)
        if self.category:
            self.category = normalize_catrgory(self.category)

       # Generate a unique slug and remove stop words
        original_slug = slugify(self.title)
        stop_words = ["a", "an", "the", "and", "in", "on", "with", "of", "etc"]
        words = original_slug.split("-")
        cleaned_slug = "-".join([word for word in words if word not in stop_words])
        queryset = Blog.objects.filter(slug__iexact=cleaned_slug)
        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        # Handle slug conflicts
        count = 1
        slug = cleaned_slug
        while queryset.filter(slug=slug).exists():
            slug = f"{cleaned_slug}-{count}"
            count += 1
        self.slug = slug

        # Ensure only one blog is featured at a time
        if self.featured:
            try:
                temp = Blog.objects.get(featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Blog.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def _get_old_thumbnail(self):
        if self.pk:
            return Blog.objects.get(pk=self.pk).thumbnail
        return None

    def get_absolute_url(self):
        return reverse('detailview', kwargs={'category': self.category, 'slug': self.slug})

    @property
    def blogid(self):
        return self._id


class Comment(models.Model):
    name = models.CharField(
        max_length=255, default=None, blank=True, null=True)
    email = models.EmailField(
        max_length=255, default=None, blank=True, null=True)
    subject = models.CharField(
        max_length=255, default=None, null=True, blank=True)
    comment = models.TextField(null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"comment author name {self.name}, comment author email {self.email}"

    class Meta:
        ordering = ['-created']


class Contact(models.Model):
    _id = models.CharField(default=random_id_generator,
                           blank=True, null=False, primary_key=True, max_length=900)
    username = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    email = models.EmailField(default=None, blank=True, null=True)
    subject = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"user with id {self._id} and name {self.username} contacted around {self.created}"
