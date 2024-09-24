from django.urls import path
from .views import ItemView

urlpatterns = [
    path('', ItemView.as_view(), name='create_item'),
    path('<int:item_id>/', ItemView.as_view(), name='item'),
    # path('update/<int:item_id>/', UpdateItemView.as_view(), name='update_item'),
    # path('delete/<int:item_id>/', DeleteItemView.as_view(), name='delete_item'),
]
