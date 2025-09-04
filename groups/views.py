# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        try:
            group = Group.objects.create(
                name=name,
                description=description,
                owner=request.user
            )
            group.members.add(request.user)
            messages.success(request, 'Group created successfully!')
            return redirect('groups:group_detail', group_id=group.id)
        except Exception as e:
            messages.error(request, f'Error creating group: {str(e)}')
            
    return render(request, 'groups/create_group.html')

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    context = {
        'group': group,
        'is_owner': request.user == group.owner,
        'member_count': group.get_members_count()
    }
    return render(request, 'groups/group_detail.html', context)

@login_required
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    # Check if user is the owner
    if request.user != group.owner:
        messages.error(request, "You don't have permission to edit this group.")
        return redirect('groups:group_detail', group_id=group_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        group.name = name
        group.description = description
        group.save()
        
        messages.success(request, 'Group updated successfully!')
        return redirect('groups:group_detail', group_id=group_id)
        
    return render(request, 'groups/edit_group.html', {'group': group})
