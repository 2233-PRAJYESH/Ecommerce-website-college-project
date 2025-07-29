

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, GroupProductShare
from store.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        group = Group.objects.create(name=name, owner=request.user)
        group.members.add(request.user)
        return redirect('group_detail', group_id=group.id)
    return render(request, 'groups/create_group.html')

@login_required
def share_product(request, group_id, product_id):
    group = get_object_or_404(Group, id=group_id)
    product = get_object_or_404(Product, id=product_id)
    if request.user in group.members.all():
        GroupProductShare.objects.create(group=group, product=product, shared_by=request.user)
    return redirect('group_detail', group_id=group.id)

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    shares = group.groupproductshare_set.all()
    return render(request, 'groups/group_detail.html', {'group': group, 'shares': shares})
