from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Chat, GroupChat, Relationship, GroupMessage
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

import json

# Create your views here.
@login_required
def index(request):
    users, current_user, other_person = get_chat_details(request)
    
    context = {
        "users":users,
        "current_user":current_user.id,
        "chats":other_person
    }
    return render(request, 'chat/index.html', context)

@login_required
def room(request, room_name):
    users, current_user, other_person = get_chat_details(request)

    # Setting user1, user2
    user1 = request.user
    user2 = User.objects.get(id=room_name)

    context = {
        "room_name": room_name,
        "user2": user2.username,
        "users": users,
        "current_user": current_user.id,
        "chats": other_person
    }
    return render(request, 'chat/room.html', context)

# View to handle group chat
def group_chat(request, group_name=None):
    current_user = request.user
    # Fetching user and his/her associated groups
    user = User.objects.get(username=request.user)
    groupsQuerySet = GroupChat.relationship.through.objects.filter(user=user)
    
    # Constructing groups list to send to the client-side
    groups = []
    for group in groupsQuerySet:
        groups.append(group.group.group_name)

    # Fetching messages of the group
    try:
        group_chat = None or list(GroupChat.objects.get(group_name=group_name))
        messages = None or list(GroupMessage.objects.filter(chat_id=group_chat.group_id))
    except:
        messages = None
    
    context = {
        "groups": groups,
        "current_user": current_user.username,
        "messages": messages or None,
        "current_group": group_name
    }
    return render(request, 'chat/groupchat.html', context)

# Create a new group
def create_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Get group name from request and create new group entry
        group_name = data['group_name']
        groupObj = GroupChat(group_name=group_name)
        groupObj.save()

        # Get users from request and add entries in Relationship table
        users = data['users']
        for user in users:
            userObj = User.objects.get(username=user)
            Relationship.objects.create(user=userObj, group=groupObj)
        
        return JsonResponse({'message': 'Group created successfully'})

    return JsonResponse({'message': 'Invalid request method'})

# Add new member to the group
def add_to_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Get group name and users and add them to the group
        users = data['users']
        group_name = data['group_name']

        groupObj = GroupChat.objects.get(group_name=group_name)
        for user in users:
            userObj = User.objects.get(username=user)
            Relationship.objects.create(user=userObj, group=groupObj)
        return JsonResponse({'message': 'Added to group successfully'})

    return JsonResponse({'message': 'Invalid request method'})

# Exit from the group
def exit_group(request):
    pass

# Utility function to fetch users, current_user, chats, other_person
def get_chat_details(request):
    # Fetching all users list
    users = list(User.objects.values("username", "id"))
    current_user = User.objects.get(id=request.user.id)

    # Fetching all chats of current user
    chats = Chat.objects.filter(
                Q(user1=current_user) | Q(user2=current_user)
            )
    chats = list(chats.values())

    # Making a list of all persons the current user has chatted with
    other_person = []
    for chat in chats:
        if chat['user1_id'] == current_user.id:
            op = User.objects.filter(id=chat["user2_id"]).values('username').first()
        else:
            op = User.objects.filter(id=chat["user1_id"]).values('username').first()
        other_person.append(op['username'])
    
    return [users, current_user, other_person]

