from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import CommentForm, EmailPostForm
from .models import Post


def post_list(request):
    """
    List all published posts with pagination of 3 posts per page and
    handling wrong values for page numbers
    """

    # Retrieve all published posts.
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(...)
    page_number = request.GET.get(...)
    try:
        posts = ...
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = ...
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = ...
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, year, month, day, post):
    """
        Retrieve a published post by its date and slug
    """
    post = get_object_or_404(
        Post,
        status=...,
        slug=...,
        publish__year=...,
        publish__month=...,
        publish__day=...,
    )
    # List of active comments for this post
    comments = ...
    # Form for users to comment
    form = ...

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        },
    )


class PostListView(ListView):
    """
    Alternative post list view
    """

    queryset = ...
    context_object_name = 'posts'
    paginate_by = ...
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrieve a published post by id
    post = get_object_or_404(
        Post,
        id=...,
        status=...
    )

    # send/share the post to an email address specified by user.
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = ...
            post_url = request.build_absolute_uri(
                ...
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=...,
                message=...,
                from_email=None,
                recipient_list=[...],
            )
            sent = True

    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        },
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=...,
        status=...
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = ...
        # Assign the post to the comment
        comment.post = ...
        # Save the comment to the database
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        },
    )
