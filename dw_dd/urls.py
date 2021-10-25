from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from.import views
from account import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.main), #초기페이지
    path('Base/',views.main),
    path('login/',account_views.login, name ='login'),
    path('refreshBTN', views.refreshBTN, name="refreshBTN"),

    path('GL_Page/SearchResult', views.Search_EQ, name="Search_EQ_HTML"),
    path('GL_Page/SearchResult2', views.GL_Result, name="Search_GL_BTN"),
    path('login_next/',views.login_next),
]
