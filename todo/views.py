from django.shortcuts import render
from .models import Todo
from .forms import TodoForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    todos = request.user.todo_set.all().filter(title__contains=request.GET.get('search',''))
    context = {
        'todos': todos,
    }
    return render(request, 'todo/index.html', context)

@login_required
def view(request, id):
    todo = Todo.objects.get(id=id)
    context = {
        'todo': todo
    }
    return render(request, 'todo/detail.html', context)

@login_required
def edit(request, id):
    todo = Todo.objects.get(id=id)
    
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {
            'form': form,
            'id': id
        }      
        return render(request, 'todo/edit.html', context)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance = todo)
        if form.is_valid():
            form.save()
        messages.success(request, 'Tarea actualizada')
        context = {
            'form': form,
            'id': id
        }  
        return render(request, 'todo/edit.html', context)
    

@login_required
def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo')
    else:
        form = TodoForm()
    return render(request, 'todo/create.html', {'form': form})

@login_required
def delete(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect('todo')