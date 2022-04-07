from django.views.generic import ListView, DetailView
from .models import Post, Category


# Create your views here.

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