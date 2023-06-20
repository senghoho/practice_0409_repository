from django.db import models
# Django의 User 모델 호출
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    name=models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    body = models.TextField()
    progress = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    like = models.ManyToManyField(User, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)


    def __str__(self):
        return self.title
    
    def summary(self):
        return self.body[:20]

class Comment(models.Model):
    content = models.TextField()
    pub_date = models.DateTimeField()
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title+" : "+self.content[:20]