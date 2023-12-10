from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import uuid
from django.db import models
from django.utils.encoding import smart_str
from .models import UploadedFile
from datetime import datetime
import time
import copy

from . import algo
from .models import Record

def store_file_and_generate_id(file):
    # 生成一个唯一的文件标识符
    file_upload_id = str(uuid.uuid4())
    file.name = f"{file_upload_id}_{file.name}"
    # 存储文件到服务器的文件系统或数据库
    uploaded_file = UploadedFile(file=file)
    uploaded_file.save()
    # 返回标识符
    return file_upload_id

def get_first_file_by_id(file_upload_id):
    try:
        # 用 UUID 构建预期的文件名前缀
        print(file_upload_id)
        # filename_prefix = f"{file_upload_id}_"
        filename_prefix = f"uploads/{file_upload_id}_"
        # 过滤出所有文件名以该 UUID 开头的 UploadedFile 对象
        matching_files = UploadedFile.objects.filter(file__startswith=filename_prefix)
        if matching_files:
            # 如果有多个匹配项，取第一个
            return matching_files.first().file.path
        else:
            # 如果没有匹配项，返回 None 或抛出异常
            print("没找到匹配项")
            return None
    except ValueError:
        # 如果提供的 UUID 格式不正确
        print("uuid格式错误")
        return None

def process_files(train_file_path, predict_file):
    # 在这里实现两个文件的处理逻辑
    # 例如合并文件，处理数据等
    train_res = algo.train(train_file_path)
    predict_res = algo.test(predict_file)
    # print(train_res)
    # print(predict_res)
    ret = {**train_res, **predict_res}
    # save_dic = copy.deepcopy(ret)
    # current_time =datetime.now()
    # time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
    # save_dic['id'] = time_str
    # record = Record(data=save_dic)
    # record.save()
    print(ret)
    return ret
    


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
    print("训练文件标识符：" + file_upload_id)
    return JsonResponse({'fileUploadId': file_upload_id})


def upload_predict_file(request):
    file = request.FILES.get('file')
    file_upload_id = request.POST.get('fileUploadId')
    # 找到第一个文件
    first_file = get_first_file_by_id(file_upload_id)
    if not first_file and file:
        print("找不到训练文件")
        return JsonResponse({'error': '找不到第一个文件'}, status=400)

    # 在这里一起处理两个文件
    time.sleep(10)
    ret = process_files(first_file, file)    

    return JsonResponse(ret)

def download_file(request):
    file_path = '/home/junj/2023_autumn/Software_Engineering/backend/download/predict.json'
    with open(file_path, 'rb') as f:
        response = HttpResponse(f, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename="%s"' % smart_str(file_path)
        response['X-Sendfile'] = smart_str(file_path)
        return response

def getRecord(request):
    records = Record.objects.all()
    data_list = list(records.values('data'))
    return JsonResponse(data_list, safe=False)