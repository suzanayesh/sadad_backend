
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.shortcuts import render
from .models import RootUser



# List all users
def Root_User_List(request):
    rootusers = RootUser.objects.all()
    return render(request, 'root_user_list.html', {'rootusers': rootusers})

# Create a new user
def Root_User_Create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password_hash = request.POST.get('password_hash')
        if username and password_hash:
            RootUser.objects.create(username=username, password_hash=password_hash)
            return redirect('Root_User_List')
    return render(request, 'root_user_form.html')

# Update an existing user
def Root_User_Update(request, pk):
    user = get_object_or_404(RootUser, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.password_hash = request.POST.get('password_hash', user.password_hash)
        user.save()
        return redirect('Root_User_List')
    return render(request, 'root_user_form.html', {'user': user})

# Delete a user
def Root_User_Delete(request, pk):
    user = get_object_or_404(RootUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('Root_User_List')
    return render(request, 'root_user_confirm_delete.html', {'user': user})



