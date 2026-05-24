from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Task, UserProfile
from .forms import TaskForm, UserProfileForm, UserForm
from django.contrib.auth.models import User

# Create your views here.
@login_required
def task_list(request):

    # Show/filter only tasks belonging to the current user.

    # tasks = Task.objects.filter(user=request.user)
    tasks = Task.objects.all()
    
    users = User.objects.all() 

    # Empty form for adding new task
    form = TaskForm()

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'form': form,
        'users': users,
        'user': request.user
    })
# one resusable 
def task_access(user, task):
    return (
        user.is_superuser or
        task.created_by == user or
        user in task.assigned_to.all()
    )


@login_required
def create_task(request):
    
    # Handle creation of a new task using Django Form.
    
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            # form.save()
            task = form.save(commit=False)#create task object, dont save#form not including all model fieds

            # attacking task to logged in user, 
            task.created_by = request.user

            task.save() #saving task to db INSERT INTO Task_table(title, user_id,..)

            form.save_m2m()

    return redirect('task_list')


@login_required
def update_task(request, task_id):
    
    task = get_object_or_404(Task, id=task_id)
    # task = Task.objects.get(id=task_id)

    # Authorization check # only update your task.
    # if task.user != request.user and not request.user.is_superuser:
    #     return HttpResponseForbidden("You cannot edit this task.")

    if not task_access(request.user, task):
        return HttpResponseForbidden()

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'completed', 'rejected']:
        
            task.status = new_status
            task.save()
        

    return redirect('task_list')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # task = Task.objects.get(id=task_id)

   # edit permission check, edit by only owner or superadmin
    if not task_access(request.user, task):
        return HttpResponseForbidden()

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            task.title = title
            task.save()

    return redirect('task_list')


@login_required
def delete_task(request, task_id):
   
    task = get_object_or_404(Task, id=task_id)

# delete permission check, delete by only owner or superadmin
    if task.created_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You cannot delete this task.")

    task.delete()

    return redirect('task_list')

# @login_required
# def update_profile(request):
#     profile = request.user.userprofile
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid:
#             form.save()
#             return redirect ('profile')
#     else:
#         form = UserProfileForm(instance=profile)



#     return render(request, 'update_profile.html', {'form':form})


@login_required
def update_profile(request):
    # Fetch the profile instance linked to the current user
    profile = request.user.userprofile
    
    if request.method == 'POST':
        # Load data into both forms simultaneously
        # This runs ONLY when the save button is clicked
        u_form = UserForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        # Check validity for both (note the parentheses on is_valid())
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('update_profile')  # Redirect to the same page after saving
    else:
        # Pre-populate both forms with current database values
        u_form = UserForm(instance=request.user)
        p_form = UserProfileForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'update_profile.html', context)


@login_required
def assign_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    # permission check
    if not (request.user == task.created_by or request.user.is_superuser):
        return HttpResponseForbidden()

    if request.method == "POST":

        user_id = request.POST.get('assigned_user')

        print("DEBUG USER ID:", user_id)

        if user_id:

            try:
                user = User.objects.get(id=user_id)

                task.assigned_to.add(user)
                task.save()

                print("ASSIGNED SUCCESS")

            except User.DoesNotExist:
                print("USER NOT FOUND")

    return redirect('task_list')