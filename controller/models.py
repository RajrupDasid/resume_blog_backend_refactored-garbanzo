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


class Blog(models.Model):
    _id = models.CharField(default=random_string_generator,
                           blank=False, null=False, auto_created=True, max_length=900)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_location, null=True, blank=True, default=None)
    files = models.FileField(upload_to=media_file_upload,
                             null=True, blank=True, default=None, max_length=1000000000)
    slug = models.SlugField(max_length=500, unique=True)
    tags = TaggableManager(blank=True)
    content = RichTextUploadingField(default=None, blank=True, null=True)

    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Blog has been generate with id {self._id} | with title {self.title} | at {self.created}"

    def save(self, *args, **kwargs):
        if self.thumbnail:
            img = Img.open(BytesIO(self.thumbnail.read()))
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail((self.thumbnail.width / 1.5,
                          self.thumbnail.height / 1.5), Img.BOX)
            output = BytesIO()
            img.save(output, format='WebP', quality=70)
            output.seek(0)
            self.thumbnail = InMemoryUploadedFile(output, 'ImageField', "%s.webp" % self.thumbnail.name.join(
                random_string_generator()).split('.')[0:10], 'thumbnail/webp', len(output.getbuffer()), None)
        original_slug = slugify(self.title)
        queryset = Blog.objects.all().filter(slug__iexact=original_slug).count()
        count = 1
        slug = original_slug
        while (queryset):
            slug = original_slug + '-' + str(count)
            count += 1
            queryset = Blog.objects.all().filter(slug__iexact=slug).count()
        self.slug = slug
        if self.featured:
            try:
                temp = Blog.objects.get(featured=True)
                if self != temp:
                    temp.featured = False
                    temp.save()
            except Blog.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})


class Contact(models.Model):
    _id = models.CharField(default=random_id_generator,
                           blank=True, null=False, primary_key=True, max_length=900)
    username = models.CharField(
        max_length=255, blank=True, null=True, default=None)
    email = models.EmailField(default=None, blank=True, null=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"user with id {self._id} and name {self.username} contacted around {self.created}"
