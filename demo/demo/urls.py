from django.conf.urls import url 
from . import index_view,index_ERform_view,detail_view
from . import tagging_data_view,tagging_data_writefile_view
from . import _404_view, overview_view
from . import relation_view
from . import tagging
from . import question_answering, decisions_making

urlpatterns = [
    url(r'^$', index_view.index),
    url(r'^ER-post',index_ERform_view.ER_post),
    url(r'^detail', detail_view.showdetail),
    url(r'^tagging_data', tagging_data_view.showtagging_data),
    url(r'^tagging-get', tagging_data_writefile_view.tagging_push),
    url(r'^overview', overview_view.show_overview),
    url(r'^404',_404_view._404_), 
    url(r'^search_entity',relation_view.search_entity),
    url(r'^tagging',tagging.tagging),
    url(r'^search_relation',relation_view.search_relation),
    url(r'^qa', question_answering.question_answering),
    url(r'^decision', decisions_making.decisions_making)
    
]
