from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Property, ImageGroup
from django.db.models import Subquery, OuterRef, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import shutil
import os

def index(request):
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    지산 = Property.objects.filter(매물종류="지식산업센터").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    덕지산 = Property.objects.filter(매물종류="덕지식산업센터").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    향지산 = Property.objects.filter(매물종류="향지식산업센터").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    아파트 = Property.objects.filter(매물종류="아파트").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    오피스텔 = Property.objects.filter(매물종류="오피스텔").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    상가 = Property.objects.filter(매물종류="상가").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    사무실 = Property.objects.filter(매물종류="사무실").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    # 다가구 = Property.objects.filter(매물종류="다가구/2룸/3룸").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    # 점포 = Property.objects.filter(매물종류="점포주택매매").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]
    # 토지 = Property.objects.filter(매물종류="토지").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')[:8]

    context = {
        "지산" : 지산,
        "아파트" : 아파트,
        "오피스텔" : 오피스텔,
        "상가" : 상가,
        "사무실" : 사무실,
        "덕지산" : 덕지산,
        "향지산" : 향지산,
    }
    
    return render(request, "mom/index.html", context)

def ajax_login(request):
    # AJAX 요청인지 확인
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # POST 요청인지 확인
        if request.method == 'POST':
            # 사용자 이름과 비밀번호 가져오기
            username = request.POST.get('username')
            password = request.POST.get('password')
            # 사용자 인증
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # 인증 성공: 사용자 로그인
                login(request, user)
                # 로그인 성공 응답
                return JsonResponse({"success": True})
            else:
                # 인증 실패: 오류 메시지
                return JsonResponse({"success": False, "error": "로그인 실패! 비밀번호를 확인해주세요"})
    # 잘못된 요청 응답
    return JsonResponse({"success": False, "error": "유효하지 않은 요청"})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def sells(request):
    return render(request, "mom/sell.html")

@login_required
def sells_upload(request):
 
    if request.method == 'POST':
        인기 = request.POST.get('인기') == 'true'
        강력추천 = request.POST.get('강력추천') == 'true'
        급매 = request.POST.get('급매') == 'true'
        저렴 = request.POST.get('저렴') == 'true'
        신축 = request.POST.get('신축') == 'true'
        추천 = request.POST.get('추천') == 'true'
        즉시입주 = request.POST.get('즉시입주') == 'true'

        공면 = request.POST.get('공급면적')
        전면 = request.POST.get('전용면적')
        공치 = str(round(float(공면) * 3.306, 2))
        전치 = str(round(float(전면) * 3.306, 2))
        


        property = Property(
            제목 = request.POST.get('제목'),
            지역 = request.POST.get('지역'),
            매물종류 = request.POST.get('매물종류'),
            거래종류 = request.POST.get('거래종류'),
            매매가 = request.POST.get('가격'),
            매매가억 = request.POST.get('가격억'),
            월세 = request.POST.get('월세'),
            테마 = request.POST.get('테마'),
            공급면적 = 공면,
            공면치환 = 공치,
            공면가격 = request.POST.get('공면가격'),
            전용면적 = 전면,
            전면치환 = 전치,
            전면가격 = request.POST.get('전면가격'),
            방향 = request.POST.get('방향'),
            해당층 = request.POST.get('해당층'),
            전체층 = request.POST.get('전체층'),
            난방 = request.POST.get('난방'),
            주차 = request.POST.get('주차'),
            주차비 = request.POST.get('주차비'),
            입주일 = request.POST.get('입주일'),
            사용승인일 = request.POST.get('사용승인일'),
            네이버주소 = request.POST.get('주소'),
            내용 = request.POST.get('content'),
        )
        
        if 인기:
            property.인기 = 인기
        if 강력추천:
            property.강력추천 = 강력추천
        if 급매:
            property.급매 = 급매
        if 신축:
            property.신축 = 신축
        if 추천:
            property.추천 = 추천
        if 저렴:
            property.저렴 = 저렴
        if 즉시입주:
            property.즉시입주 = 즉시입주


        property.save()
        print('성공')

        # 업로드된 파일 처리
        files = request.FILES.getlist('files')

        for file in files:
            image_instance = ImageGroup(property=property, 이미지=file)
            image_instance.save()

        return redirect('sells')

 
        # 클라이언트에 오류 메시지 반환
    return render(request, "mom/sell.html")

def detail(request, id):
    property = get_object_or_404(Property, id=id)
    images = ImageGroup.objects.filter(property=id)
    
    context = {
        '매물': property,
        '사진': images,
    }

    return render(request, "mom/detail.html", context)

def jisan(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    지산 = Property.objects.filter(매물종류="지식산업센터").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(지산, items_per_page)
    try:
        지산 = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = 지산.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        지산 = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        지산 = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(지산.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "지산": 지산
    }

    return render(request, "mom/m_jisan.html", context)

def apart(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    아파트 = Property.objects.filter(매물종류="아파트").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(아파트, items_per_page)
    try:
        아파트 = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = 아파트.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        아파트 = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        아파트 = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(아파트.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "아파트": 아파트
    }

    return render(request, "mom/m_apart.html", context)

def officetel(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    오피스텔 = Property.objects.filter(매물종류="오피스텔").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(오피스텔, items_per_page)
    try:
        오피스텔 = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = 오피스텔.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        오피스텔 = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        오피스텔 = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(오피스텔.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "오피스텔": 오피스텔
    }

    return render(request, "mom/m_officetel.html", context)

def sanga(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    상가 = Property.objects.filter(매물종류="상가").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(상가, items_per_page)
    try:
        상가 = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = 상가.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        상가 = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        상가 = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(상가.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "상가": 상가
    }

    return render(request, "mom/m_sanga.html", context)

def office(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    오피스 = Property.objects.filter(매물종류="사무실").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(오피스, items_per_page)
    try:
        오피스 = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = 오피스.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        오피스 = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        오피스 = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(오피스.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "오피스": 오피스
    }

    return render(request, "mom/m_office.html", context)

def multi(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    다가구 = Property.objects.filter(매물종류="덕지식산업센터").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(다가구, items_per_page)
    try:
        다가구 = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = 다가구.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        다가구 = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        다가구 = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(다가구.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "다가구": 다가구
    }

    return render(request, "mom/m_multi.html", context)

def store(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    점포 = Property.objects.filter(매물종류="향지식산업센터").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(점포, items_per_page)
    try:
        점포 = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = 점포.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        점포 = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        점포 = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(점포.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "점포": 점포
    }

    return render(request, "mom/m_store.html", context)

def land(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    # Property 쿼리셋에 첫 번째 이미지 URL을 annotate
    토지 = Property.objects.filter(매물종류="토지").annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(토지, items_per_page)
    try:
        토지 = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = 토지.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        토지 = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        토지 = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(토지.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "토지": 토지
    }

    return render(request, "mom/m_land.html", context)

@login_required
@require_http_methods(["POST"])
def delete_property(request):
    property_id = request.POST.get('property_id')
    if not property_id:
        return JsonResponse({'error': 'No property ID provided.'}, status=400)

    property = get_object_or_404(Property, pk=property_id)
    red = ''
    match property.매물종류:
        case '지식산업센터':
            red = 'jisan'
        case '아파트':
            red = 'apart'
        case '오피스텔':
            red = 'officetel'
        case '상가':
            red = 'sanga'
        case '사무실':
            red = 'office'
        case '덕지식산업센터':
            red = 'multi'
        case '향지식산업센터':
            red = 'store'
        case '토지':
            red = 'land'
    folder_path = f'media/images/{property.업로드_시간.strftime(r"%Y%m%d-%H%M%S")}'

    property.delete()  # Property 인스턴스 삭제

    # 폴더 삭제
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

    return redirect(red)  # 삭제 후 리다이렉트

@login_required
def sell_update(request, id):
    property = get_object_or_404(Property, id=id)
    images = ImageGroup.objects.filter(property=id).order_by("id")
    image_urls = [settings.MEDIA_URL + img.이미지.name for img in images]

    context = {
        "매물" : property,
        "사진" : images,
        "image_urls": image_urls,  # 이미지 URL 목록을 컨텍스트에 추가
    }

    if request.method == 'POST':
        # Boolean 필드 업데이트
        인기 = request.POST.get('인기') == 'true'
        강력추천 = request.POST.get('강력추천') == 'true'
        급매 = request.POST.get('급매') == 'true'
        저렴 = request.POST.get('저렴') == 'true'
        신축 = request.POST.get('신축') == 'true'
        추천 = request.POST.get('추천') == 'true'
        즉시입주 = request.POST.get('즉시입주') == 'true'


        # 면적 계산 후 업데이트
        공면 = request.POST.get('공급면적')
        전면 = request.POST.get('전용면적')
        property.공급면적 = 공면
        property.전용면적 = 전면
        property.공면치환 = str(round(float(공면) * 3.306, 2))
        property.전면치환 = str(round(float(전면) * 3.306, 2))

        # 나머지 필드 업데이트
        property.제목 = request.POST.get('제목')
        property.지역 = request.POST.get('지역')
        property.매물종류 = request.POST.get('매물종류')
        property.거래종류 = request.POST.get('거래종류')
        property.매매가 = request.POST.get('가격')
        property.매매가억 = request.POST.get('가격억')
        property.월세 = request.POST.get('월세')
        property.테마 = request.POST.get('테마')
        property.공면가격 = request.POST.get('공면가격')
        property.전면가격 = request.POST.get('전면가격')
        property.방향 = request.POST.get('방향')
        property.해당층 = request.POST.get('해당층')
        property.전체층 = request.POST.get('전체층')
        property.난방 = request.POST.get('난방')
        property.주차 = request.POST.get('주차')
        property.주차비 = request.POST.get('주차비')
        property.입주일 = request.POST.get('입주일')
        property.사용승인일 = request.POST.get('사용승인일')
        property.네이버주소 = request.POST.get('주소')
        property.내용 = request.POST.get('content')

        if 인기:
            property.인기 = 인기
        if 강력추천:
            property.강력추천 = 강력추천
        if 급매:
            property.급매 = 급매
        if 신축:
            property.신축 = 신축
        if 추천:
            property.추천 = 추천
        if 저렴:
            property.저렴 = 저렴
        if 즉시입주:
            property.즉시입주 = 즉시입주

        property.save()  # 변경사항 저장

        

        # 새로운 이미지 추가
        files = request.FILES.getlist('files')

        images_one = images.first()
        folder_path = f'media/images/{images_one.created_at.strftime(r"%Y%m%d-%H%M%S")}' # 수정 전 이미지 그룹 폴더 경로 추출

        images.delete() # 이미지 그룹 데이터 삭제

        if os.path.exists(folder_path): # 이미지 그룹 폴더 삭제
            shutil.rmtree(folder_path)

        for file in files:
            image_instance = ImageGroup(property=property, 이미지=file) # 새로운 이미지 그룹 생성
            image_instance.save()

        redirect_url = f'detail/{id}'
        return JsonResponse({'success': True, 'redirect_url': redirect_url})
    
    return render(request, "mom/sell_update.html", context)

def search(request):
    items_per_page = 8 # 한 페이지에 보여줄 아이템의 수
    page = request.GET.get('page', 1) # 현재 페이지 번호를 쿼리 파라미터에서 가져오거나, 없으면 1로 설정
    # 썸네일 서브쿼리
    # OuterRef를 사용하여 외부 쿼리(Property)의 기본 키(pk)를 참조
    thumbnail = ImageGroup.objects.filter(property=OuterRef('pk')).order_by('created_at').values('이미지')[:1] # annotate로 붙이기 위해 값만 가져온다.
    
    query = request.GET.get('search','')

    if query:
        # Q 객체를 사용하여 OR 조건으로 필터링합니다.
        q_objects = Q(매물종류__icontains=query) | Q(거래종류__icontains=query) | \
                    Q(매매가억__icontains=query) | Q(테마__icontains=query) | Q(내용__icontains=query) | Q(매매가__icontains=query) | Q(제목__icontains=query) | Q(지역__icontains=query)
                    
        # 생성된 Q 객체로 쿼리셋을 필터링하고, .distinct()로 중복을 제거합니다.
        results = Property.objects.filter(q_objects).distinct().annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')
        
    else:
        results = Property.objects.all().annotate(first_image_url=Subquery(thumbnail)).order_by('-업로드_시간')  # 비어 있는 쿼리셋을 반환합니다.

    # Paginator를 사용하여 페이지네이션 설정
    paginator = Paginator(results, items_per_page)
    try:
        results = paginator.page(page) # 요청된 페이지에 해당하는 매물을 가져옴
        is_last_page = results.has_next() is False # 다음 페이지가 없으면 마지막 페이지임
    except PageNotAnInteger:
        results = paginator.page(1) # 페이지 번호가 정수가 아니면 첫 페이지를 로드
        is_last_page = False
    except EmptyPage: # 요청된 페이지 번호가 범위를 벗어나면 마지막 페이지 로드
        results = paginator.page(paginator.num_pages)
        is_last_page = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        properties_list = list(results.object_list.values('id', '거래종류', 'first_image_url', '매매가억', '매매가', '월세', '지역', '제목', '전면치환', '해당층', '전체층', '추천', '강력추천', '인기', '신축', '즉시입주', '급매', '저렴'))
        return JsonResponse({"properties": properties_list, "is_last_page": is_last_page}, safe=False)

    context = {
        "결과": results,
        "검색어": query,
    }

    return render(request, "mom/search.html", context)

def page_not_found(request, exception):
    return render(request, 'mom/404error.html', {})

