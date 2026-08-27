from django.db import models


# Create your models here.

class Blog(models.Model):
    title = models.CharField()
    content = models.TextField()
    image = models.ImageField(upload_to="blogs/")
    date = models.DateField(auto_now_add=True)
    published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
