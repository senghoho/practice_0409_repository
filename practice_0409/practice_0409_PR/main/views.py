from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Tag
from django.utils import timezone

# Create your views here.

def detail(request, id):
    post = get_object_or_404(Post, pk = id)
    if request.method == 'GET':
        # filter에 post 객체 그대로 넣어주기
        comments = Comment.objects.filter(post=post)
        return render(request, 'main/detail.html',{
            'post':post,
            'comments':comments,
        })
    elif request.method == "POST":
        new_comment = Comment()
        # foreignkey > blog 객체 직접 넣어주기
        new_comment.post = post
        # foreignkey > request.user 객체 직접 넣어주기
        new_comment.writer = request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()
        new_comment.save()
        return redirect('main:detail', id)

    return render(request, 'main/detail.html',{'post':post})


def mainpage(request):
    posts = Post.objects.all()
    return render(request, 'main/mainpage.html', {'posts':posts})

def secondpage(request):
    return render(request, 'main/secondpage.html')


def create(request):
    # 만약 로그인 된 상태면? 게시물 저장
    if request.user.is_authenticated:
        new_post = Post()
        new_post.title = request.POST['title']
        # new_blog의 writer 필드에 현재 로그인 한 유저 저장
        new_post.writer = request.user
        new_post.pub_date = timezone.now()
        new_post.body = request.POST['body']
        new_post.progress = request.POST['progress']
        new_post.image = request.FILES.get('image')
        new_post.save()
        # 본문의 내용을 띄어쓰기로 잘라낸다
        words = new_post.body.split(' ')
        # 만약 단어가 공백이 아니고 #으로 시작하면, #을 뗀 후 tag_list에 저장한다
        tag_list = []
        for w in words:
            if len(w)>0:
                if w[0]=='#':
                    tag_list.append(w[1:])
        # 해시태그가 들어있는 tag_list를 하나씩 돌면서
        for t in tag_list:
            # 기존에 존재하는 태그면 get, 없으면 create
            tag, boolean = Tag.objects.get_or_create(name=t)
            # 이후 태그 필드에 추가
            new_post.tags.add(tag.id)
        return redirect('main:detail', new_post.id)
    # 로그인 안했으면? 로그안 하러가라
    else:
        return redirect('accounts:login')



def new(request):
    return render(request, 'main/new.html')

# 수정 화면으로 가는 코드 구현
def edit(request, id):
    edit_post = Post.objects.get(id=id)
    return render(request, 'main/edit.html', {'post': edit_post})

# update(수정) 기능 구현
def update(request, id):
    if request.user.is_authenticated:
        update_post = Post.objects.get(id=id)
        if request.user == update_post.writer:
            update_post.title = request.POST['title']
            update_post.pub_date = timezone.now()
            update_post.body = request.POST['body']
            update_post.image = request.FILES.get('image', update_post.image)
            update_post.save()
            return redirect('main:detail', update_post.id)
    return redirect('accounts:login')

# delete(삭제) 기능 구현
def delete(request, id):
    delete_post = Post.objects.get(id=id)
    delete_post.delete()
    return redirect('main:mainpage')

# 모든 tag 리스트를 볼 수 있는 페이지 구현
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'main/tag_list.html', {
        'tags':tags,
    })

# 태그 선택 시 해당 태그가 포함된 게시물 보는 기능 구현
def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = tag.posts.all()
    return render(request, 'main/tag_posts.html',{
        'tag':tag,
        'posts':posts,
    })

# 댓글 삭제
def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    if request.user == comment.writer:
        comment.delete()
    return redirect('main:detail' ,comment.post.id)