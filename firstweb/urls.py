from django.urls import path,re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from firstweb import views

app_name='firstweb'

urlpatterns = [
    url(r'login/$',auth_views.LoginView.as_view(template_name='firstweb/login.html'),name='login'),
    url(r'logout/$',auth_views.LogoutView.as_view(),name='logout'),
    url(r'signup/$',views.SignUp,name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'search_status/$',views.search_status,name='search_status'),
    #url(r'^update/(?P<pk>\d+)/$',views.Update.as_view(),name='update')
    url(r'profile/$',views.profile,name='profile'),
    url(r'reset_password/',auth_views.PasswordResetView.as_view(template_name='firstweb/password_reset.html'),name='reset_password'),
    url(r'reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    url(r'reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    url(r'reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    url(r'password_change/',auth_views.PasswordChangeView.as_view(template_name='firstweb/password_change_form.html'),name='password_change'),
    url(r'stud/(?P<status>[\w-]+)/$',views.Stud,name='stud'),
    #url(r'stud/$',views.Stud,name='stud'),
    url(r'chat/$',views.chat,name='chat'),
    url(r'change-friends/(?P<username>\w+)/$',views.change_friends,name='change_friends'),
    #url(r'messages/$',views.messages,name='messages'),
    #url(r'test/index/$', views.index, name='index'),
    #path('test/index/', views.index, name='index'),
    url(r'chat/(?P<username>[\w.@+-]+)/$',views.ThreadView.as_view()),
]