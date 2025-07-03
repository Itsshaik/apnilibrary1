from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
   # path('login/', views.login_view, name='login'),
    #path('logout/', views.logout_view, name='logout'),
   # path('register/', views.register, name='register'),
    path('serve_pdf/<int:note_id>/', views.serve_pdf, name='serve_pdf'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),

    path('create_class/', views.create_class, name='create_class'),
    path('create_subject/<int:class_id>/', views.create_subject, name='create_subject'),
    path('upload/<int:subject_id>/', views.upload_note, name='upload_note'),

    path('view_pdf/<int:note_id>/', views.view_pdf, name='view_pdf'),
    path('download_pdf/<int:note_id>/', views.download_pdf, name='download_pdf'),

    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('delete_subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('delete_class/<int:class_id>/', views.delete_class, name='delete_class'),
    path('classes', views.class_list, name='class_list'),
    path('subjects', views.subject_list, name='subject_list'),
    path('notes', views.notes_list, name='notes_list'),
    path('search/', views.search, name='search'),
]