from django.db.models import get_model
from django.views.generic import DetailView, ListView

Post = get_model('blog', 'Post')


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/post_list.html'
