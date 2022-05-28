from django.db.models.fields import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import mixins
from rest_framework import response
from rest_framework.response import Response
from .serializers import *
from .models import Note
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class NotesGetList(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Note.objects.all()
    def get(self, request):
        notes=Note.objects.filter(owner=request.user)
        serializer=NoteSerializer(notes,many=True)
        response=[]
        for i in serializer.data:
            note = Note.objects.get(id=i['id'])
            response.append({
                'id': note.id,
                'title': note.title,
                'color':note.color,
                'creator': note.owner.username,
                'created':note.created,
                'desc': note.desc,
            })
        return Response(response,status=status.HTTP_200_OK)

class NoteDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    lookup_field = 'id'
    def put(self, request, id=None):
        try:
            note = Note.objects.get(id__exact=id)
        except:
            return Response({"Note with the following id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Note.objects.filter(Q(owner=request.user))
        x = False
        for notes in queryset:
            if notes == note:
                x = True
        if x:
            return self.update(request, id)
        else:
            return Response({"You dont have permission to edit/view this note"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, id=None):
        try:
            note = Note.objects.get(id__exact=id)
        except:
            return Response({"Note with the following id does not exist"} , status=status.HTTP_404_NOT_FOUND)

        response=[]
        if note.owner==request.user:
            response.append({
                'id': note.id,
                'title': note.title,
                'color':note.color,
                'created':note.created,
                'desc': note.desc,
            })
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"You dont have permission to view this todo"}, status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, id):
        try:
            note = Note.objects.get(id__exact=id)
        except:
            return Response({"Note with the following id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        queryset = Note.objects.filter(Q(owner=request.user))
        x = False
        for notes in queryset:
            if notes == note:
                x = True
        if x:
            return self.destroy(request, id)
        else:
            return Response({"You dont have permission to delete this todo"}, status=status.HTTP_403_FORBIDDEN)


class NoteCreateView(generics.GenericAPIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # uncomment the above line to check in postman
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = NoteCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = serializer.save()
        return Response({
            "id": id,
        }, status=status.HTTP_201_CREATED)
# Create your views here.
