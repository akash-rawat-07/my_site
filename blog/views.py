from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Author, Tag, Post, Comment
from .forms import CommentForm
from django.urls import reverse

# Class Based View
from django.views.generic import ListView, DetailView
from django.views import View


# Class Based Views

class StartingPageView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name= 'blog/index.html'
    ordering = ["-date"]

    def get_queryset(self):
        base_query = super().get_queryset()
        data = base_query[:3]
        return data


class AllPostsView(ListView):
    model = Post
    context_object_name = "all_posts"
    template_name = "blog/all-posts.html"
    ordering = ["-date"]


class SinglePostView(View):
    # Our own defined method to check whether the post is already present in session or not
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        # Here checking if post stored for read later or not
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        
        return is_saved_for_later

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
        

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(Post, slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

# Logic for Read Later button
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)    # Here using special filter to get all posts stored in list
            context["posts"] = posts
            context["has_posts"] = True
        
        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")   # Using 'get' so that first time when we access it we do not get error

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])      # accessing 'post_id' from Html button

        if post_id not in stored_posts:
            stored_posts.append(post_id)    
        else:
            stored_posts.remove(post_id)
        
        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")



# Function based Views
# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {"posts": latest_posts})

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {"all_posts": all_posts})

# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)   
#     return render(request, "blog/post-detail.html", {
#         "post": identified_post,
#         "post_tags": identified_post.tags.all()
#     })
