from django.conf.urls import url 
from . import index_view,index_ERform_view,detail_view
from . import  tagging_data_view,tagging_data_writefile_view

urlpatterns = [
    url(r'^$', index_view.index),
    url(r'^ER-post',index_ERform_view.ER_post),
    url(r'^detail', detail_view.showdetail),
    url(r'^tagging_data', tagging_data_view.showtagging_data),
    url(r'^tagging-get', tagging_data_writefile_view.tagging_push),
]