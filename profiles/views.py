from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from .forms import UserProfileForm
from django.contrib import messages
from .models import Profile
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
@login_required
def profile_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    if not request.user.is_authenticated():
        raise Http404

    if Profile.objects.filter(slug=request.user.username).exists():
        return redirect('../' + request.user.username + '/edit')

    form = UserProfileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        print(form.cleaned_data.get("bio"))
        print(form.cleaned_data.get("avatar"))
        instance.save()
        messages.success(request, "성공적으로 게시되었습니다.")
        print("really error?")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        print("yes it is error!")
        messages.error(request, "게시에 실패하였습니다.")
    context = {
        "form": form,
    }
    return render(request, "form.html", context)

@login_required
def profile_detail(request, slug=None):
    instance = Profile.objects.get(slug=slug)
    context = {
        "title": "프로필",
        "instance": instance,
    }
    return render(request, "portfolio_detail.html", context)

@login_required
def profile_update(request, slug=None):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    instance = get_object_or_404(Profile, slug=slug)
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "instance": instance,
        "form": form,
    }
    return render(request, "form.html", context)

def profile_list(request):
    queryset_list = Profile.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct() # 검색 기능 Like %S%
    paginator = Paginator(queryset_list, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "파트너스 찾기",
        "page_request_var": page_request_var,
    }
    return render(request, "profile_list.html", context)
