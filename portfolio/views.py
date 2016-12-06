from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from .forms import PortfolioForm
from django.contrib import messages
from .models import Portfolio, Category
from comments.forms import CommentForm
from comments.models import Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

try:
    from urllib.parse import quote_plus
except:
    pass

# Create your views here.


@login_required
def portfolio_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    if not request.user.is_authenticated():
        raise Http404

    form = PortfolioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        print(form.cleaned_data.get("content"))
        print(form.cleaned_data.get("image"))
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
def portfolio_detail(request, slug=None):

    if not request.user.is_authenticated():
        raise Http404

    instance = get_object_or_404(Portfolio, slug=slug)
    share_string = quote_plus(instance.content)

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id,
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
    }
    return render(request, "portfolio_detail.html", context)


@login_required
def portfolio_update(request, slug=None):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404

    if not request.user.is_authenticated():
        raise Http404

    instance = get_object_or_404(Portfolio, slug=slug)
    form = PortfolioForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "form.html", context)


@login_required
def portfolio_delete(request, slug=None):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404

    if not request.user.is_authenticated():
        raise Http404

    instance = get_object_or_404(Portfolio, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:list")


def portfolio_list(request, slug=None):
    queryset_list = Portfolio.objects.all()
    categories = Category.objects.all()
    query = request.GET.get("q")
    category = request.GET.get("category")
    if query or category:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(category=category)
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
        "title": "포트폴리오 찾기",
        "page_request_var": page_request_var,
        "categories": categories,
    }
    return render(request, "portfolio_list.html", context)
