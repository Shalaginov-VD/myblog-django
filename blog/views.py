from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category
from .forms import CommentForm
from django.core.paginator import Paginator

def post_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    posts = Post.objects.all()
    if category_id:
        posts = posts.filter(category_id=category_id)
    if query:
        posts = posts.filter(title__icontains=query)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query, 'categories': categories})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})