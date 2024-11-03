from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "El usuario ya existe"},
                )
        else:
            return render(
                request,
                "signup.html",
                {"form": UserCreationForm, "error": "La contraseña no coincide"},
            )


def home(request):
    return render(request, "home.html")


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    # con el filtro date_completed ocultamos las tareas que ya fueron completadas
    return render(request, "tasks.html", {"tasks": tasks})


@login_required
def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "El usuario o la contraseña son incorrectos",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(
                request.POST
            )  # tomamos los datos para crear un nuevo form completo y lo guardamos
            new_task = form.save(
                commit=False
            )  # el commit false, es para que no guarde el objeto solo lo mantenga en memoria
            new_task.user = (
                request.user
            )  # aca le asignamos el usuario que creo la tarea porque hasta aca no lo habiamos hecho
            new_task.save()  # y aca si guardamos en la base de datos la info
            return redirect("tasks")
        except:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Por favor ingrese datos validos"},
            )


@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect("tasks")


@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.date_completed = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False)
    return render(request, "tasks.html", {"tasks": tasks})
