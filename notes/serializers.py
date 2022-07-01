from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from .models import Note

class NoteCreateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        data= self.validated_data
        owner = self.context['request'].user
        title = data['title']
        description=data['description']
        color=data['color']
        #created=data['created']
        note = Note.objects.create(owner=owner, title=title,description=description,color=color,)
        return note.id

    class Meta:
        model = Note
        fields = ('id', 'title', 'description','createdTime','color',)


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'description','createdTime','color')