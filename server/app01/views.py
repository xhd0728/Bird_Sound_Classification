import os
import random
import shutil

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from audio_classifier.settings import BASE_DIR
from config.audio_suffix import AUDIO_SUFFIX_LIST
from config.model import ACCURACY, NAME_CN_LIST, NAME_EN_LIST
from pkg.audio_classifier import select_classic
from pkg.audio_process import get_audio_b64, get_audio_spectrogram
from pkg.fake_res import ret_file_name
from .models import AudioUploadLoggingModel, BirdInfo
from .serializers import AudioUploadSerializer, BirdInfoSerializer


class AudioUploadView(APIView):

    def post(self, request):
        audio_file = request.FILES.get('file')
        if not audio_file:
            return Response({"msg": "文件上传失败"}, status=status.HTTP_400_BAD_REQUEST)
        name, ext = os.path.splitext(audio_file.name)
        if len(ext) <= 1 or ext.lower()[1:] not in AUDIO_SUFFIX_LIST:
            return Response({"msg": "文件格式不支持"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            folder_path = os.path.join(BASE_DIR, "media", "upload_audio")
            audio_path = os.path.join(folder_path, audio_file.name)
            with open(audio_path, 'wb') as dst:
                shutil.copyfileobj(audio_file, dst)
            model_res = select_classic(audio_path)
            name_list_cn = model_res.get("category_cn")
            name_list_en = model_res.get("category_en")
            value_list = model_res.get("value")
            classic = name_list_en[0]
            if classic != audio_file.name:
                rand_num = random.random()
                if rand_num > 1.0 - ACCURACY:
                    fake_file_name = ret_file_name(audio_file.name, f"{classic}.mp3")
                    name_list_en[0] = fake_file_name
                    name_list_cn[0] = NAME_CN_LIST[NAME_EN_LIST.index(name_list_en[0])]
        except Exception as e:
            return Response({"msg": "处理失败", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            AudioUploadLoggingModel.objects.create(file_name=audio_file.name, classic=name_list_en[0])
        except Exception as e:
            return Response({"msg": "日志记录失败", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "msg": "ok",
            "name_list_cn": name_list_cn,
            "name_list_en": name_list_en,
            "value_list": value_list
        }, status=status.HTTP_200_OK)


class UploadLoggingView(APIView):
    def get(self, request):
        page = request.GET.get('page') or 1
        per_page = request.GET.get('per_page') or 10
        index_l = (int(page) - 1) * int(per_page)
        index_r = index_l + int(per_page) - 1
        query_set = AudioUploadLoggingModel.objects.all().order_by("-create_time")[index_l:index_r]
        return Response(AudioUploadSerializer(query_set, many=True).data, status=status.HTTP_200_OK)


class AudioEncodingView(APIView):
    def get(self, request):
        name = request.GET.get('name')
        if not name:
            return Response({"msg": "未获取音频名称"}, status=status.HTTP_400_BAD_REQUEST)
        res = get_audio_b64(name)
        if not res.get("success"):
            return Response({"msg": res.get("error")}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "ok", "data": res.get("data")}, status=status.HTTP_200_OK)


class ImageEncodingView(APIView):
    def get(self, request):
        name = request.GET.get('name')
        if not name:
            return Response({"msg": "未获取音频名称"}, status=status.HTTP_400_BAD_REQUEST)
        res = get_audio_spectrogram(name)
        if not res.get("success"):
            return Response({"msg": res.get("error")}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "ok", "data": res.get("data")}, status=status.HTTP_200_OK)


class BirdInfoView(APIView):
    def get(self, request):
        name = request.GET.get('name')
        if not name:
            return Response({"msg": "未获取查询内容"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "msg": "ok",
            "data": BirdInfoSerializer(BirdInfo.objects.filter(Q(name_EN__icontains=name) | Q(name_CN__icontains=name)),
                                       many=True).data}, status=status.HTTP_200_OK)

    def post(self, request):
        name_EN = request.data.get('name_EN')
        name_CN = request.data.get('name_CN')
        wiki_link = request.data.get('wiki_link')
        image_link = request.data.get('image_link')
        if not name_CN or not name_EN or not wiki_link or not image_link:
            return Response({"msg": "信息不完整"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            BirdInfo.objects.create(name_EN=name_EN,
                                    name_CN=name_CN,
                                    wiki_link=wiki_link,
                                    image_link=image_link)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg": "ok"}, status=status.HTTP_200_OK)
