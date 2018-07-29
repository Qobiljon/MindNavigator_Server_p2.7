# coding=utf-8
"""MindNavigator_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url

from MindNavigator_Server import views
from MindNavigator_Server.models import Intervention, InterventionManager

urlpatterns = [
    url('admin/', admin.site.urls),
    url('log_fetch$', views.handle_log_fetch),
    url('user_reg$', views.handle_register),
    url('user_lgn$', views.handle_login),
    url('event_crt$', views.handle_event_submit),
    url('event_edt$', views.handle_event_edit),
    url('event_del$', views.handle_event_delete),
    url('event_del$', views.handle_event_delete),
    url('events_fetch$', views.handle_events_fetch),
    url('interv_crt$', views.handle_intervention_submit),
    url('interv_syst$', views.handle_system_intervention_fetch),
    url('interv_peer$', views.handle_peer_intervention_fetch),
    url('eval_subm$', views.handle_evaluation_submit),
    url('eval_fetch$', views.handle_evaluation_fetch),
    url('surv_subm$', views.handle_survey_submit),
    url('surv_fetch$', views.handle_survey_fetch),
]

if Intervention.objects.all().count() == 0:
    Intervention.objects.create_intervention(name=u"밖에 나가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"쇼핑 또는 물건 사기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"이야기, 잡지, 뉴스 읽기 또는 듣기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"음악 듣기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"TV 보기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"웃기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"친구 또는 가족들과 식사하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"간식 만들기 또는 간식 먹기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"집 주변 정리하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"가족들과 함께 있지", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"가장 좋아하는 옷 입기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"새소리, 바람, 파도 등 자연의 소리 듣기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"편지 또는 카드 써서 보내기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"공원, 피크닉 등 외출하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"커피나 차를 친구들과 마시기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"칭찬 듣기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"걷기, 춤추기 등 운동하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"드라이브 가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"화장, 면도, 머리 깎기 등 꾸미기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"과거 일들을 회상하거나 이야기하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"비싼 옷 또는 갖추어진 옷 입기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"종교 단체, 자선 단체 또는 기타 단체에 기부하기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"스포츠에 대해 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"같은 성별의 새로운 사람 만나기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"준비가 잘 된 시험 보기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"록 콘서트 보러가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"야구나 소프트볼 놀이하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"여행 또는 휴가 계획 세우기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"나를 위해 무언가 사기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"바다 보러가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"예술 작품 만들기 (그림, 색칠, 조각, 영화 만들기 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"암벽 등반이나 등산", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"경전이나 다른 성스러운 작품 읽기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"골프치기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"군 생활 참여하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내 방이나 집을 정리하거나 꾸미기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"나체로 있기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"스포츠 행사 참여 또는 보러가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"자기계발도서 읽기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"경주 (말, 자동차, 보트 등) 보러가기 ",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"이야기, 소설, 시 또는 연극 읽기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"술집, 주점, 클럽 등에 가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"수업 또는 연설 들으러가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"능숙하게 운전하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"맑은 공기 마시기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"음악을 생각하거나 노래 정리하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"술 마시기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"명확하게 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"배타기 (카누 타기, 카약 타기, 모터보트 타기, 요트 타기 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"부모님 기쁘게 하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"골동품 복원 또는 가구 재정비하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"나 자신에게 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"캠핑가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"정치에서 일하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"기계 작업 (자동차, 자전거, 오토바이, 트랙터 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"미래에 일어날 좋은 일에 대해 생각하기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"카드 게임하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"어려운 작업 끝내기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"문제 해결 (퍼즐, 크로스워드 퀴즈 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"결혼식에 참석하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가 비판하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"친구 또는 동료들과 점심먹기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"테니스치기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"샤워하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"먼 거리 운전하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"나무로 작업하기 (목공)", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"이야기, 소설, 연극 또는 시 쓰기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"동물들과 같이 있기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"비행기 타기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"탐험 (알려진 도로에서 멀어지기, 등산 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"솔직하고 열린 대화 하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"그룹에서 노래하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"나 자신 또는 자신의 문제에 대해 생각해보기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"직장에서 일하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"파티에 참석하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"교회 행사 참석하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"외국어 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"봉사, 시민 또는 사교클럽 모임에 가기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"비즈니스 회의 또는 대회 참가하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"스포츠 카 또는 비싼차 타기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"악기 연주하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"간식 만들기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"스노우 스키 타기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"도움 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"비공식적인 복장 착용하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"머리를 빗거나 닦기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"연극하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"낮잠자기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"친구들과 함께 있기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"통조림,  냉동 등 식품 보존하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"과속해서 운전하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"개인적인 문제 해결하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"욕조에서 목욕하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"나를 위한 노래부르기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"판매할 음식이나 공예품 만들기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"당구치기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"컴퓨터 게임하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"체스 게임하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"공예품 만들기 (도자기, 보석, 가죽, 구슬, 직조 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"몸무게 재기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"자신의 몸 긁기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"화장하거나 머리손질하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"설계 또는 제도 (디자인)", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"아프거나 곤경에 처한 사람들 방문하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"응원하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"볼링치기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"모임에서 인기 얻기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"야생 동물 관찰하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"독창적인 생각하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"원예, 조경, 또는 마당 작업", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"에세이 또는 전문적인 문학 읽기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"새로운 옷 입기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"햇볕에 앉아있기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"오토바이 타기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"그냥 앉아서 생각하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사람들과 함께 술마시기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내 가족이나 친구들에게 좋은 일이 일어나길 기대하기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"박람회, 축제, 서커스, 동물원, 유원지 등 가기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"철학이나 종교에 대해 이야기하기 ", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"무언가 계획 또는 조직하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"혼자 술마시기 (혼술)", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"자연의 소리 듣기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"데이트하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"활발히 이야기하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"자동차, 오토바이, 보트 등의 경주", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"라디오 듣기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"친구들 초대 또는 초청하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"스포츠 경기에서 경쟁하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내가 좋아하는 사람들 소개하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"선물 주기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"학교 또는 정부 회의, 법원 회의 등에 참석하기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"마사지 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"편지, 카드 또는 메모 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"하늘, 구름, 폭풍 지켜보기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"외출하기 (공원, 피크닉, 바베큐 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"농구하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"우리 가족을 위해 뭔가 사기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사진찍기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"연설이나 강연하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"지도 읽기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"자연물 수집 (야생 식품 또는 과일, 암석, 유목지 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내 재정 관리", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"깨끗한 옷 입기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"주요 구매 또는 투자 (자동차, 가전 제품, 주택, 주식 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가 돕기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"산속에 있기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"직장에서 발전하기 (승진, 인상, 더 나은 직업 제공, 더 나은 학교 입학 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"농담 듣기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내기 이기기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"자녀 또는 손주들에 대해 이야기하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"새로운 이성의 사람 만나기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내 건강에 대해 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"아름다운 풍경보기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"좋은 음식 먹기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"건강 개선 (치아 고정, 새 안경 복용, 식사 변경 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"시내 나가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"레슬링 또는 권투", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사냥 또는 사격", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"뮤지컬 그룹에서 연주하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"하이킹", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"박물관이나 전시 보러가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"논문, 수필, 기사, 보고서, 메모 등 쓰기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"일 잘하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"여가 시간 보내기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"낚시 하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"뭔가 빌려주기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"성적인 매력으로 주목 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"고용주, 교사 등을 기쁘게해주기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가 상담하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"헬스 클럽, 사우나, 목욕탕 등에 가기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가 나를 비판하게하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"새로운 것을 배우기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"맥도날드, 버거킹, 스타벅스 등 'drive through' 가기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가 칭찬하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내가 좋아하는 사람들에 대해 생각하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가에게 복수하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"부모님과 함께하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"승마", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사회, 정치 또는 환경 적 조건에 대한 항의",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"전화로 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"백일몽", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"나뭇잎, 모래, 자갈 등을 걷어차기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"잔디 스포츠 (예 : 배드민턴, 크로켓, 셔플 보드, 말굽 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"학교 동창회, 동창회 등 참석하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"유명한 사람들보기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"영화 보러 가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"키스", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"혼자 시간 보내기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"시간 계획 세우기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"요리하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내가 존경하는 사람들로부터 칭찬 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내 인생에서 영적인 존재 느끼기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내 방식대로 프로젝트하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"집 주변에서 \"특이한 일\"하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"울기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내가 필요한 곳에 가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"가족 동창회 또는 모임에 참석하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"모임을 갖기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"머리 감기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가를 코칭하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"레스토랑에 가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"꽃이나 식물을 보거나 냄새 맡기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"초대 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"영예받기 (시민, 군대 등)", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"향수 또는 애프터 셰이브 사용하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"나에게 동의하는 사람 찾기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"옛날 이야기, 회상하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"아침 일찍 일어나기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"평화롭고 조용한 시간 보내기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"실험이나 다른 과학적 연구하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"친구들 방문하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"일기 쓰기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"축구", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"상담 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"기도하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"마사지 해주기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"히치 하이킹", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"명상 또는 요가하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"싸움보기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사람들에게 호의 베풀기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"직장 또는 학급에있는 사람들과 이야기하기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"여유 가지기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"도움이나 조언해주기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"다른 사람들의 문제에 대해 생각하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"보드 게임하기 (모노 폴리, 스크래블 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"밤에 푹 자기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"힘든 실외 작업 (목재 절단, 도마, 토지 개간, 농장 작업 등)",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"신문 읽기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사람들을 놀라게하고, 욕설을 퍼붓고, 외설스러운 몸짓하기 등",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"눈에서 스노우모빌 타기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"신체 인식, 감수성, 만남, 치료 받기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"탁구", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"이빨 닦기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"수영", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"싸우기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"조깅, 달리기, 체조, 피트니스 또는 현장 연습하기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"맨발로 걷기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"집안일이나 빨래하기 (물건 정리하기)", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내 룸메이트와 함께하는 것", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"음악 듣기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"언쟁하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"뜨개질, 크로 셰 뜨개질, 자수 또는 고급 바느질 작업",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사람들 재밌게 해주기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"섹스에 대해 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"이발사 또는 미용사에게 가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"집에 손님 들이기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사랑하는 사람과 함께 있기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"잡지 읽기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"늦게 자기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"새 프로젝트 시작하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"고집부리기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"파트너와 성관계 갖기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"다른 성적인 만족감을 갖기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"도서관가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"축구, 럭비, 하키, 라크로스 등을 즐기기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"새롭거나 특별한 음식 준비하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"새 관찰하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"쇼핑하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사람들 구경하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"화재 신고", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"논쟁에서 이기기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"판매 또는 거래하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"프로젝트 또는 작업 마무리", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"고백 또는 사과하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"고장난 것 수리하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"팀으로 다른 사람들과 협력하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"자전거 타기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사람들에게 무엇을 해야할지 알려주기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"행복한 사람들과 함께하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"파티하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"편지, 카드 또는 메모 작성하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"정치 또는 공무에 대해 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"도움이나 조언 요청하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"연회, 오찬, 주점 등", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"취미 또는 특별한 관심사에 대해 이야기하기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"매력적인 여성 또는 남성 시청", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"모래, 개울, 풀밭에서 놀기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"다른 사람들에 대해 이야기하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"남편 또는 아내와 함께하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"견학, 자연 산책 등", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가에게 내 사랑을 표현하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"담배 피우기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"실내 식물 관리", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"친구와 함께 커피, 차, 콜라 등 마시기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"물건 모으기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"핸드볼, 패들볼, 스쿼시 등", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"재봉", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"떠난 친구 또는 사랑하는 사람 기억하기, 공동 묘지 방문하기",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"아이들과 함께하는 일", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"바닷가에서 생활하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"간식 먹기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"늦게까지 자지 않기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"경매, 차고 판매 등", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"흥미로운 질문에 대해 생각하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"자원 봉사 활동, 지역 사회 봉사 프로젝트 작업",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"수상 스키, 서핑, 스쿠버 다이빙", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"돈 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가를 방어하거나 보호하기, 사기 또는 남용 중지",
                                             intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"좋은 설교 듣기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"경쟁에서 이기기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"새 친구 사귀기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"내 직업 또는 학교에 대해 말하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"만화, 코믹 스트립 또는 만화책 읽기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"무언가 빌리기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"단체 여행하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"옛 친구 구경하기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"누군가 가르치기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"여행", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"사무실 파티 참석", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"콘서트, 오페라 또는 발레에 참석", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"애완 동물과 놀기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"연극에 가기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"별이나 달 보기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
    Intervention.objects.create_intervention(name=u"코칭 받기", intervention_type=InterventionManager.SYSTEM,
                                             creation_method=InterventionManager.SYSTEM)
