from django.contrib import admin
from django.urls import path
from artwork import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.paintings_list, name='paintings_list'),  # объединенный маршрут для списка и поиска
    path('painting/<int:id>/', views.painting_detail, name='painting_detail'),
    path('order/<int:order_id>/', views.view_order, name='order_summary'), 
]
