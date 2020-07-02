from django.urls import path
from backend.views import views,information,User_view,detailpage,vidio,dic_user,home,test


urlpatterns = [

# views
    path('index/', views.index),
    path('index_xiala/',views.index_xiala),
    path('news_detail/', views.news_detail),
    path('scheduler_bot/', views.scheduler_bot),
    path('scheduler_top/', views.scheduler_top),

# information
    path('score_info/',information.score_info),
    path('top_player/',information.top_player),

#用户登录
    path('authorize/',User_view.authorize),

# 详情页 新闻点赞
    path('detail_praise/',detailpage.newsprice),

#详情页，收藏
    path('shoucang/',detailpage.shoucang),
    path('send_comment/',detailpage.send_comment),

#  点赞评论
    path('comment_price/',detailpage.comment_price),
    path('comment_detail/',detailpage.comment_detail),

# 视频
    path('vidio_list/',vidio.vidio),
    path('click_video/',vidio.click_video),
    path('click_dianshou/',vidio.click_dianshou),
    path('fenxiang/',vidio.fenxiang),

#用户ip地址
    path('dic_user/',dic_user.dic_user),

# bad_user页面
    path('bad_user/',dic_user.bad_user),

# 视频分享页面
    path('share_url/',vidio.share_url),
#weixin_top
    # path('weixin_top/',home.weixin_top),

#home页面数据
    path('home_information/',home.home_date),

#测试
    path('test/',test.test)
]
