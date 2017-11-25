from django.conf.urls import url 
from . import index_view,index_ERform_view,detail_view
 
urlpatterns = [
    url(r'^$', index_view.index),
    url(r'^ER-post',index_ERform_view.ER_post),
    url(r'^detail', detail_view.showdetail),
]