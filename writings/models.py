from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Writing(models.Model):
    format = models.TextField(verbose_name='형식')
    purpose = models.TextField(verbose_name='목적')
    writer = models.ForeignKey(to=User,on_delete=models.CASCADE)

class Paragraph(models.Model):
    index = models.TextField(verbose_name='목차')
    content = models.TextField(verbose_name='내용')
    bookmark = models.BooleanField(verbose_name='즐겨찾기',default=False)
    writing = models.ForeignKey(to=Writing,on_delete=models.CASCADE,related_name='paragraphs')