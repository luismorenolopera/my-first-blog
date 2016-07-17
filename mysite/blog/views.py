from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


from .forms import PostForm, CommentForm, UserForm
from .models import Post, Comment


class PostList(ListView):
    model = Post


class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    model = Post
    permission_required = 'blog.add_post'
    fields = ['title', 'text']
    template_name = 'blog/base_form.html'
    login_url = '/access_denied/'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data(**kwargs)
        context['message'] = 'New Post'
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    permission_required = 'blog.change_post'
    fields = ['title', 'text']
    template_name = 'blog/base_form.html'
    login_url = '/access_denied/'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data(**kwargs)
        context['message'] = 'Edit Post'
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'blog.delete_post'
    login_url = '/access_denied/'
    success_url = reverse_lazy('post_list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/base_form.html', {'form': form,
                                                   'message': 'New Comment'})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


def user_new(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserForm()
    return render(request, 'blog/base_form.html', {'form': form,
                                                   'message': 'New User'})


def access_denied(request):
    return render(request, 'blog/access_denied.html')
