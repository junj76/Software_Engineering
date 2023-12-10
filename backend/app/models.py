from django.db import models
from django.db.models import JSONField  # 从Django 3.1开始使用
import uuid

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # 假设你将文件保存在 media/uploads/ 目录下
    created_at = models.DateTimeField(auto_now_add=True)
    
class Record(models.Model):
    data = JSONField()