from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist.models import TaskList
from todolist.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            form.save()
        messages.success(request, ("new task added"))
        return redirect("todolist")
    else:

        all_task = TaskList.objects.all()
        paginator = Paginator(all_task, 5)
        page = request.GET.get("pg")
        all_task = paginator.get_page(page)

        return render(request, "todolist.html", {"all_task": all_task})


def contact(request):
    context = {"welcome_text": "welcome to contact page"}
    return render(request, "contact.html", context)


def about(request):
    context = {"welcome_text": "welcome to about us page"}
    return render(request, "about.html", context)


def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)

    task.delete()
    return redirect("todolist")


def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
        messages.success(request, ("Task edited"))
        return redirect("todolist")

    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, "editt.html", {"task_obj": task_obj})


def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)

    task.done = True
    task.save()
    return redirect("todolist")


def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)

    task.done = False
    task.save()
    return redirect("todolist")
