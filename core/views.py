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
    tasks = Task.objects.all().order_by('-created_at')
    
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

   # edit permission check, edit by only owner, assigned user or superadmin
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



@login_required
def assign_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    # permission check
    if not (request.user == task.created_by or request.user.is_superuser):
        return HttpResponseForbidden()

    if request.method == "POST":

        user_id = request.POST.get('assigned_user')

        if user_id:

            try:
                user = User.objects.get(id=user_id)

                task.assigned_to.add(user)
                task.save()

                

            except User.DoesNotExist:
                print("USER NOT FOUND")

    return redirect('task_list')



def signup(request):

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = UserForm()

    return render(
        request,
        'registration/signup.html',
        {'form': form}
    )

@login_required
def update_profile(request):

    profile = request.user.userprofile

    # getting tasks created by the logged in user from the DB
    my_tasks = Task.objects.filter(
        created_by=request.user
    )

    # getting tasks assigned to the logged in user from the DB
    assigned_tasks = Task.objects.filter(
        assigned_to=request.user
    )

    # getting all users from the DB to show in the dropdown for assigning tasks
    users = User.objects.all()


# processing form submission for updating user profile
    if request.method == 'POST':

        u_form = UserForm(
            request.POST,
            instance=request.user
        )

        p_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()

            return redirect('update_profile')

    else:

        u_form = UserForm(instance=request.user)

        p_form = UserProfileForm(instance=profile)

    context = {

        'u_form': u_form,
        'p_form': p_form,

        'my_tasks': my_tasks,
        'assigned_tasks': assigned_tasks,

        'my_tasks_count': my_tasks.count(),
        'assigned_tasks_count': assigned_tasks.count(),

        'users': users
    }

    return render(
        request,
        'update_profile.html',
        context
    )

