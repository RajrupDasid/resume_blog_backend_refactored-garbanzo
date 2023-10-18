from rest_framework import serializers
from .models import Blog, Contact

from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)



class BlogViewSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Blog
        fields = '__all__'


class BlogDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Blog
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
