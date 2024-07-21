from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Author(models.Model):
    full_name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rating = 0
        for post in self.post_set.all():
            posts_rating += post.rating
        posts_rating = posts_rating * 3

        author_comments_rating = 0
        for comment in self.user.comment.all():
            author_comments_rating += comment.rating

        posts_comments_rating = 0
        for post in self.post_set.all():
            for comment in post.comment_set.all():
                posts_comments_rating += comment.rating

        self.rating = posts_rating + author_comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=10, choices=[('article', 'Статья'), ('news', 'Новость')], default='article')
    date_create = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        return f"{self.text[:123]}..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date_create = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1


