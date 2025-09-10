from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group

@login_required
def create_group(request):
    """
    Handles the creation of a new group.
    Requires a logged-in user to access.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name:
            try:
                # Use 'created_by' instead of 'owner' and remove 'description'
                group = Group.objects.create(
                    name=name,
                    created_by=request.user
                )
                group.members.add(request.user)
                messages.success(request, 'Group created successfully!')
                return redirect('groups:group_detail', group_id=group.id)
            except Exception as e:
                print(f"Error creating group: {e}")
                messages.error(request, f"There was an error creating the group: {e}")

    return render(request, 'groups/create_group.html')

@login_required
def group_detail(request, group_id):
    """
    Displays the details of a single group.
    """
    group = get_object_or_404(Group, id=group_id)
    context = {
        'group': group,
        # Check if the user is the one who created the group
        'is_creator': request.user == group.created_by,
        'member_count': group.members.count()
    }
    return render(request, 'groups/group_detail.html', context)

@login_required
def edit_group(request, group_id):
    """
    Handles editing a group's details.
    Only the creator can edit the group.
    """
    group = get_object_or_404(Group, id=group_id)
    
    # Check if the user is the creator of the group
    if request.user != group.created_by:
        messages.error(request, "You don't have permission to edit this group.")
        return redirect('groups:group_detail', group_id=group_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        # Update the group's name
        group.name = name
        group.save()
        
        messages.success(request, 'Group updated successfully!')
        return redirect('groups:group_detail', group_id=group_id)
        
    return render(request, 'groups/edit_group.html', {'group': group})
