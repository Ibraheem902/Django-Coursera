import logging
from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from blog.forms import CommentForm
from .models import Post
# Create your views here.
logger = logging.getLogger(__name__)


def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now())
    logger.debug('Got %d posts', len(posts))
    return render(request, 'blog/index.html', {'posts': posts})
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.creator = request.user
                comment.content_object = post
                comment.save()
                logger.warning("Logging is working!")
                logger.info('Created comment on Post %d for user %s',post.pk, request.user)#Give us the post id and user who made the comment
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, 'blog/post-detail.html', {'post': post, 'comment_form': comment_form})
