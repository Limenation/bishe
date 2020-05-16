from django.conf.urls import url
from django.urls import path


from .views import CoursesListView, CourseDetailView, CourseVideoView, CourseCommentView,VideoPlayView

urlpatterns = [
    # 课程列表
    path('list/', CoursesListView.as_view(), name='list'),

    # 课程详情
    path('detail/<int:course_id>/', CourseDetailView.as_view(), name='detail'),

    # 章节列表，点击开始学习时出现的视频列表
    path('video/<int:course_id>/', CourseVideoView.as_view(), name='video'),

    # 课程评论
    path('comment/<int:course_id>/', CourseCommentView.as_view(), name='comment'),

    # 视频播放
    path('play/<int:video_id>/', VideoPlayView.as_view(), name='play'),

]