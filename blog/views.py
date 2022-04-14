from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Category, Tag


# Create your views here.

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=Post
    fields = ['title', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.request.user.is_superuser or self.request.user.is_staff) :
            form.instance.author = self.request.user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog')

class PostList(ListView):
    model = Post
    ordering = '-pk'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['category_less_post_count'] = Post.objects.filter(category=None).count()

        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['category_less_post_count'] = Post.objects.filter(category=None).count()

        return context
#
# def index(request):
#     posts = Post.objects.all()
#     return render(request, 'blog/index.html',
#                   {
#                       'posts' : posts,
#                   }
#     )
#
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk = pk)
#
#
#     return render(request, 'blog/post_detail.html', {'post':post})
def cagegories_page(request, slug):
    if slug=='no-category':
        category='미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug = slug)
        post_list = Post.objects.filter(category = category)

    context = {
        'categories' : Category.objects.all(),
        'category_less_post_count' : Post.objects.filter(category=None).count(),
        'category' : category,
        'post_list' : post_list
    }
    return render(request, 'blog/post_list.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug = slug)
    post_list = tag.post_set.all()

    context = {
        'categories' : Category.objects.all(),
        'category_less_post_count' : Post.objects.filter(category=None).count(),
        'tag' : tag,
        'post_list' : post_list
    }
    return render(request, 'blog/post_list.html', context)