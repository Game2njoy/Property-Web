from django.db import models
from django.utils.timezone import now
import os

def get_custom_filename(instance, filename):
    """
    파일명을 현재 날짜와 시간으로 설정하되, 원본 파일의 확장자는 유지합니다.
    """
    ext = filename.split('.')[-1]
    # 파일명 예시: 20240322-152030.jpg
    filename = '{}.{}'.format(now().strftime(r'%Y%m%d-%H%M%S'), ext)
    return f'images/{now().strftime(r"%Y%m%d-%H%M%S")}/{filename}'

class Property(models.Model):
    제목 = models.CharField(max_length=255)
    지역 = models.CharField(max_length=255)
    매물종류 = models.CharField(max_length=255)
    거래종류 = models.CharField(max_length=255)
    매매가 = models.CharField(max_length=255)
    매매가억 = models.CharField(max_length=255, blank=True)
    월세 = models.CharField(max_length=255, blank=True)
    테마 = models.CharField(max_length=255)
    공급면적 = models.CharField(max_length=255)
    공면치환 = models.CharField(max_length=255, blank=True)
    공면가격 = models.CharField(max_length=255, blank=True)
    전용면적 = models.CharField(max_length=255)
    전면치환 = models.CharField(max_length=255, blank=True)
    전면가격 = models.CharField(max_length=255, blank=True)
    방향 = models.CharField(max_length=255, blank=True)
    해당층 = models.CharField(max_length=255, blank=True)
    전체층 = models.CharField(max_length=255, blank=True)
    난방 = models.CharField(max_length=255, blank=True)
    주차 = models.CharField(max_length=255, blank=True)
    주차비 = models.CharField(max_length=255, blank=True)
    입주일 = models.CharField(max_length=255, blank=True)
    사용승인일 = models.CharField(max_length=255, blank=True)
    네이버주소 = models.CharField(max_length=255, blank=True)
    업로드_시간 = models.DateTimeField(auto_now_add=True)
    추천 = models.BooleanField(default=False)
    인기 = models.BooleanField(default=False)
    강력추천 = models.BooleanField(default=False)
    신축 = models.BooleanField(default=False)
    즉시입주 = models.BooleanField(default=False)
    급매 = models.BooleanField(default=False)
    저렴 = models.BooleanField(default=False)
    내용 = models.TextField(blank=True)
    호수 = models.CharField(max_length=255, blank=True, null=True)

class ImageGroup(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    이미지 = models.ImageField(upload_to=get_custom_filename)
    created_at = models.DateTimeField(auto_now_add=True)
