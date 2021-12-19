from django.urls import path
from .views import home_page, stock_add, stock_update, stock_delete, stock_detail, detail_view

app_name = "people"

urlpatterns = [
    path('<int:pk>/', home_page, name='homepage'),
    path('<int:pk>/add/', stock_add, name='add-stock'),
    path('<int:pk>/update/', stock_update, name='update-stock'),
    path('<int:pk>/delete/', stock_delete, name='delete-stock'),
    path('<int:pk>/detail/', stock_detail, name='detail-stock'),
    path('<int:pk>/detail/view/', detail_view, name='detail-view'),

    

]