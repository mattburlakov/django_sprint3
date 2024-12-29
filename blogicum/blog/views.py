from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from django.http import Http404


def index(request):
    now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]

    return render(request, 'blog/index.html', {'post_list': posts})


def category_posts(request, category_slug):
    now = timezone.now()
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.filter(
        category=category,
        pub_date__lte=now,
        is_published=True
    ).order_by('-pub_date')

    return render(
        request,
        'blog/category.html',
        {'post_list': posts, 'category': category}
    )


def post_detail(request, post_id):
    now = timezone.now()
    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        pub_date__lte=now
    )

    if not post.category.is_published:
        raise Http404("Category is not published.")

    return render(request, 'blog/detail.html', {'post': post})
