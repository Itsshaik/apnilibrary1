from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.conf import settings
import os

from .models import Class, Subject, Note
#from .forms import RegisterForm, LoginForm

def is_admin(user):
    return user.is_authenticated and user.is_admin


# List all classes
def class_list(request):
    classes = Class.objects.all().order_by("-created_at")
    return render(request, 'classes.html', {'classes': classes})

def subject_list(request):
    subjects = Subject.objects.select_related('class_ref').all().order_by("-id")
    return render(request, 'subjects.html', {'subjects': subjects})

def notes_list(request):
    notes = Note.objects.select_related('subject').all().order_by("-uploaded_at")
    return render(request, 'notes.html', {'notes': notes})

def index(request):
    query = request.GET.get("q", "")
    if query:
        classes = Class.objects.filter(name__icontains=query)
        subjects = Subject.objects.filter(name__icontains=query)
        notes = Note.objects.filter(title__icontains=query)
        return render(request, "index.html", {
            "classes": classes,
            "subjects": subjects,
            "notes": notes,
            "search_query": query
        })
    classes = Class.objects.all().order_by("-created_at")
    notes = Note.objects.all().order_by("-uploaded_at")[:6]
    return render(request, "index.html", {
        "classes": classes,
        "recent_notes": notes,
    })

"""def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("index")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

# views.py

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Login successful.")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')"""

def class_detail(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    subjects = class_obj.subjects.all()
    return render(request, "class_detail.html", {
        "class_obj": class_obj,
        "subjects": subjects
    })

@user_passes_test(is_admin)
def create_class(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name:
            Class.objects.create(name=name, description=description)
            return redirect("index")
    return HttpResponse("Only POST allowed")

@user_passes_test(is_admin)
def create_subject(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name:
            Subject.objects.create(name=name, description=description, class_ref=class_obj)
    return redirect("class_detail", class_id=class_id)

"""def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    notes = subject.notes.all()
    return render(request, "subject_detail.html", {
        "subject": subject,
        "notes": notes
    })
    # views.py

    for note in notes:
        note.file_size_mb = round(note.file_size / (1024 * 1024), 1) if note.file_size else 0.0"""

def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    notes = subject.notes.all()

    for note in notes:
        note.file_size_mb = round(note.file_size / (1024 * 1024), 1) if note.file_size else 0.0

    return render(request, "subject_detail.html", {
        "subject": subject,
        "notes": notes
    })
@user_passes_test(is_admin)
def upload_note(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        uploaded_file = request.FILES.get("file")

        if uploaded_file:
            file_path = os.path.join("notes", uploaded_file.name)
            save_path = os.path.join(settings.MEDIA_ROOT, file_path)

            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            with open(save_path, 'wb+') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            Note.objects.create(
                title=title,
                description=description,
                subject=subject,
                filename=file_path,
                original_filename=uploaded_file.name,
                file_path=file_path,
                file_size=uploaded_file.size
            )
            return redirect("subject_detail", subject_id=subject_id)
    return render(request, "upload.html", {"subject": subject})

"""def view_pdf(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    file_path = os.path.join(settings.MEDIA_ROOT, note.filename)
    if os.path.exists(file_path):
        return render(request, "pdf_viewer.html", {"note": note})
    return HttpResponse("PDF not found")"""

def view_pdf(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    file_path = note.file.path  # Use the FileField's path
    if os.path.exists(file_path):
        return render(request, "pdf_viewer.html", {"note": note})
    return HttpResponse("PDF not found")

"""def download_pdf(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    file_path = os.path.join(settings.MEDIA_ROOT, note.filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=note.original_filename)
    return HttpResponse("PDF not found")"""

def download_pdf(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    file_path = note.file.path  # Use FileField's full path
    if os.path.exists(file_path):
        filename = os.path.basename(note.file.name)  # This gets the original uploaded filename
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    return HttpResponse("PDF not found")

@user_passes_test(is_admin)
def delete_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    subject_id = note.subject.id
    note.delete()
    return redirect("subject_detail", subject_id=subject_id)

@user_passes_test(is_admin)
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    class_id = subject.class_ref.id
    subject.delete()
    return redirect("class_detail", class_id=class_id)

@user_passes_test(is_admin)
def delete_class(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)
    class_obj.delete()
    return redirect("index")

def search(request):
    query = request.GET.get("q", "")
    classes = Class.objects.filter(name__icontains=query)
    subjects = Subject.objects.filter(name__icontains=query)
    notes = Note.objects.filter(title__icontains=query)
    return render(request, "index.html", {
        "classes": classes,
        "subjects": subjects,
        "notes": notes,
        "search_query": query
    })

def serve_pdf(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return FileResponse(note.file.open('rb'), content_type='application/pdf')