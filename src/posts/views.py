from django.db.models import Count, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author
from .forms import CommentForm, PostForm
from marketing.models import Signup



def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save() 

    context = {
        'post_list' : featured,
        'latest' : latest
    }
    return render(request, 'index.html', context)

def get_author(user):
    author = Author.objects.filter(user=user)
    if author.exists():
        return author[0]
    return None

def get_category_count():
    cat_count = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return cat_count

def blog(request):
    latest_posts = Post.objects.order_by('-timestamp')[:2]
    post_list = Post.objects.all().order_by('-timestamp')
    category_count = get_category_count()

    paginator = Paginator(post_list, 4)
    page = request.GET.get('page')
    paged_list = paginator.get_page(page)

    context = {
        'post_list' : paged_list,
        'latest_posts': latest_posts,
        'cat_count': category_count,
    }
    return  render(request, 'blog.html', context)

def search(request):
    queryset  = Post.objects.all()
    words = request.GET.get('q')

    if words:
        queryset = queryset.filter(
            Q(title__icontains=words) | 
            Q(overview__icontains=words)
        ).distinct()

    context = {
        "queryset" : queryset
    }

    return render(request, 'search_result.html', context)

def post(request, id):
    queryset = get_object_or_404(Post, pk=id)
    latest_posts = Post.objects.order_by('-timestamp')[:2]
    category_count = get_category_count()
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = queryset
            form.save()
            return redirect(reverse('post', kwargs={'id': queryset.id}))

    context = {
        'post' : queryset,
        'latest_posts': latest_posts,
        'cat_count': category_count,
        'form' : form,
    }
    return  render(request, 'post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)

def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("blog"))

    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('blog'))
