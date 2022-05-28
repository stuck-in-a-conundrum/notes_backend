from django.urls import path
#from rest_framework.urlpatterns import format_suffix_patterns
from notes import views
from notes.serializers import NoteCreateSerializer

urlpatterns = [
    path('notes/', views.NotesGetList.as_view()),
    path('notes/<int:id>/', views.NoteDetail.as_view()),
    path('note/create/', views.NoteCreateView.as_view()),
    
]