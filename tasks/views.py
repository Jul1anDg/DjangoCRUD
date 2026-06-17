from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def indexHome(request):
    return render(request, 'home.html')

def signUp(request):
    if request.method == 'GET':
        return render(request, 'signUp.html', {
            'form': UserCreationForm()
        })
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            messages.success(request, '¡Usuario creado exitosamente!')
            auth_login(request,user)
            return redirect('tasks')
        else:
            return render(request, 'signUp.html', {
                'form': form
            })
            
@login_required
def tasks(request):
    Tasks = Task.objects.filter(created_by=request.user,date_completed__isnull=True)#Muestra solo las tareas no completadas 
    return render(request, 'tasks.html', {'Tasks': Tasks})

@login_required
def signOut(request):
    logout(request)
    return redirect('home')

def signIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            auth_login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signIn.html', {
                'form': form,
                'error': '¡Usuario o contraseña incorrectos!'
            })
    else:
        form = AuthenticationForm()
    return render(request, 'signIn.html', {
        'form': form
    })
    
@login_required
def createTask(request):
   if request.method == 'GET':
       return render(request, 'createTask.html', {
           'form': TaskForm()
       })
   else:
       form = TaskForm(request.POST)
       if form.is_valid():
           task = form.save(commit=False)
           task.created_by = request.user
           task.save()            
           return render(request, 'tasks.html', {
                'msg': '¡Tarea creada exitosamente!'
           })
       else:
           return render(request, 'createTask.html', {
               'form': form,
               'msg': '¡Error al crear la tarea!'
           })
           
@login_required       
def taskDetail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, created_by=request.user)
        form = TaskForm(instance=task)
        return render(request, 'taskDetail.html',{'task': task,'form':form})
    else:
        try:
            task= get_object_or_404(Task, pk=task_id, created_by=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')  
        except ValueError:
            return render(request, 'taskDetail.html',{'task': task,'form':form, 'error':"Error actualizando los campos "})
        
@login_required            
def taskComplete(request,task_id):
    task= get_object_or_404(Task,pk=task_id, created_by=request.user)
    if request.method == 'POST':
        task.date_completed =timezone.now()
        task.completed = True
        task.save()
        return redirect('tasks')
    else:
       return render(request,'taskDetail.html')
   
@login_required
def taskDelete(request,task_id):
    task= get_object_or_404(Task,pk=task_id, created_by=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    else:
       return render(request,'taskDetail.html')
   
@login_required  
def tasksCompleted(request):
    Tasks = Task.objects.filter(created_by=request.user,date_completed__isnull=False)#Muestra solo las tareas no completadas 
    return render(request, 'tasksCompleted.html', {'Tasks': Tasks})    