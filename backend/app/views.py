from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import uuid
from .models import UploadedFile

def store_file_and_generate_id(file):
    # 生成一个唯一的文件标识符
    file_upload_id = str(uuid.uuid4())
    # 存储文件到服务器的文件系统或数据库
    uploaded_file = UploadedFile(file=file)
    uploaded_file.save()
    # 返回标识符
    return file_upload_id

def get_first_file_by_id(file_upload_id):
    # 根据ID检索文件
    try:
        uploaded_file = UploadedFile.objects.get(pk=file_upload_id)
        return uploaded_file.file.path  # 或者返回整个 UploadedFile 对象
    except UploadedFile.DoesNotExist:
        return None

def process_files(first_file_path, second_file):
    # 在这里实现两个文件的处理逻辑
    # 例如合并文件，处理数据等
    pass


def get(request):
    # return HttpResponse("Welcome")
    d = {
        'name': 'junj',
        'age': 20,
        'sex': 'male'
    }
    return JsonResponse(d)

@api_view(['POST'])
def post(request):
    if request.method == 'POST':
        received_data = request.data
        print('Received Data:', received_data)
        
        # Process the data...
        
        # Send response back to Vue.js
        response_data = {'message': 'Data received successfully!'}
        return Response(response_data, status=status.HTTP_200_OK)
    

def upload_train_file(request):
    file = request.FILES.get('file')
    # 存储文件并创建唯一标识符
    file_upload_id = store_file_and_generate_id(file)
    print("保存训练文件")
    return JsonResponse({'fileUploadId': file_upload_id})


def upload_predict_file(request):
    file = request.FILES.get('file')
    file_upload_id = request.POST.get('fileUploadId')
    # 找到第一个文件
    first_file = get_first_file_by_id(file_upload_id)
    if not first_file:
        print("找不到训练文件")
        return JsonResponse({'error': '找不到第一个文件'}, status=400)

    # 在这里一起处理两个文件
    process_files(first_file, file)
    print("成功上传训练文件、测试文件")

    return JsonResponse({'message': '两个文件已成功上传并处理'})