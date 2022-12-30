from django.urls import path
from .views import home_page, stock_add_delete, stock_update, stock_detail, detail_view, test_index

app_name = "people"

urlpatterns = [
    path('<int:pk>/', home_page, name='homepage'),
    path('<int:pk>/add-delete/', stock_add_delete, name='add/delete-stock'),
    path('<int:pk>/update/', stock_update, name='update-stock'),
    path('<int:pk>/detail/', stock_detail, name='detail-stock'),
    path('<int:pk>/detail/view/', detail_view, name='detail-view'),
    
    #testing new implementation
    path('<int:pk>/test_index', test_index, name='test_index'),

    

]