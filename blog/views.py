from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/bloghome.html', context)
    

def blogPost(request, slug):
    post = Post.objects.filter(slug= slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, 'blog/blogpost.html', context)
        
def postcomment(request):
    if request.method =='POST':
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno') 
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == '':
            comment = BlogComment(comment = comment, user = user, post = post) 
            comment.save()
            messages.success(request, "your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment = comment, user = user, post = post, parent = parent) 
            comment.save()
            messages.success(request, "your reply has been posted successfully")
    return redirect(f"/blog/{post.slug}")

def profile(request):

    context = {'user': request.user}
    return render(request,'blog/user/profile.html', context)


def profileNewPost(request):

    if request.method == 'POST':
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        slug = request.POST.get('slug')
        category = request.POST.get('category')

        #print(title,content,author,slug,category)
        if len(title) > 50:
            messages.error(request, "Title of post can be exceeded 50 chracters.")

        if len(category) > 60:
             messages.error(request, "category of post can be exceeded 60 chracters.")
            
        post = Post(title = title, content = content, author = author, slug = slug, category = category)
        post.save()
        messages.success(request, "your post has been saved successfully.")
        return redirect("/blog/profileRecentPost")
        
    context = {'user': request.user}
    return render(request,'blog/user/profileNewPost.html', context)

def profileRecentPost(request):

    allposts = Post.objects.all().filter(author = request.user.username)

    context = {'allposts':allposts, 'user': request.user}
    return render(request,'blog/user/profileRecentPost.html', context)

def profileStats(request):

    allposts = Post.objects.all().filter(author = request.user.username)

    total_views = 0

    for post in allposts:
        total_views += post.views


    postno = Post.objects.all().filter(author = request.user.username).count
    commentsno = BlogComment.objects.filter(user = request.user, parent = None).count

    context = {'user': request.user, 'postno':postno, 'commentsno': commentsno, 'viewsno': total_views}
    return render(request,'blog/user/profileStats.html', context)    
        