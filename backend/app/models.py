from django.db import models
import uuid

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # 假设你将文件保存在 media/uploads/ 目录下
    created_at = models.DateTimeField(auto_now_add=True)