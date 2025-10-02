from django.shortcuts import render, redirect, get_object_or_404
from .models import RootUser
from .serializers import RootUserSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

# List all users
def Root_User_List(request):
    rootusers = RootUser.objects.all()
    serializer = RootUserSerializer(rootusers, many=True)
    return render(request, 'root_user_list.html', {
        'rootusers': rootusers,
        'rootusers_json': json.dumps(serializer.data)
    })

# Create a new user
def Root_User_Create(request):
    serializer = RootUserSerializer()
    if request.method == 'POST':
        serializer = RootUserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('Root_User_List')
    else:
        serializer = RootUserSerializer()
    return render(request, 'root_user_form.html', {'serializer': serializer})

# Update an existing user
def Root_User_Update(request, pk):
    user = get_object_or_404(RootUser, pk=pk)
    if request.method == 'POST':
        serializer = RootUserSerializer(user, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('Root_User_List')
    else:
        serializer = RootUserSerializer(instance=user)
    return render(request, 'root_user_form.html', {'serializer': serializer, 'user': user})

# Delete a user
def Root_User_Delete(request, pk):
    user = get_object_or_404(RootUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('Root_User_List')
    return render(request, 'root_user_confirm_delete.html', {'user': user})

# API: List and create users
@csrf_exempt
def root_user_api(request):
    if request.method == 'GET':
        users = RootUser.objects.all()
        serializer = RootUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        serializer = RootUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# API: Retrieve, update, delete user by id
@csrf_exempt
def root_user_detail_api(request, pk):
    try:
        user = RootUser.objects.get(pk=pk)
    except RootUser.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        serializer = RootUserSerializer(user)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        serializer = RootUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'deleted': True})



