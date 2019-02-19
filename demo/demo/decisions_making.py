from django.shortcuts import render
import json
import os
from toolkit.img_match import get_similar_entity
from toolkit.pre_load import neo_con

relationCountDict = {}
filePath = os.path.abspath(os.path.join(os.getcwd(),"."))
with open(filePath+"/toolkit/relationStaticResult.txt","r") as fr:
    for line in fr:
        relationNameCount = line.split(",")
        relationName = relationNameCount[0][2:-1]
        relationCount = relationNameCount[1][1:-2]
        relationCountDict[relationName] = int(relationCount)
def sortDict(relationDict):
    for i in range( len(relationDict) ):
        relationName = relationDict[i]['rel']['type']
        relationCount = relationCountDict.get(relationName)
        if(relationCount is None ):
            relationCount = 0
        relationDict[i]['relationCount'] = relationCount

    relationDict = sorted(relationDict,key = lambda item:item['relationCount'],reverse = True)

    return relationDict

def decisions_making(request):  # index页面需要一开始就加载的内容写在这里
    ctx = {}
    if request.POST:
        # 连接数据库
        db = neo_con

        img_base64 = request.POST['img_base64']
        entity_list = get_similar_entity(img_base64)

        for entity in entity_list:
            answer = db.matchHudongItembyTitle(entity['label_name'])
            if len(answer) > 0:
                answer = answer[0]['n']
            else:
                entity['image'] = None
                continue
            entity['image'] = answer['image']

        for i in range(len(entity_list)-1, -1 ,-1):
            if entity_list[i]['image'] is None:
                del entity_list[i]

        best_match = ''
        best_match += '<div class="row"> <div class="col-md-3"> <a href="#" class="thumbnail">'
        best_match += '<img src="' + entity_list[0]['image'] + '" height="100%" width="100%"/></a></div>'
        best_match += '<div class="col-md-9"><h1>' + entity_list[0]['label_name'] + '</h1>'
        best_match += '</h4> 置信度：</h4>'
        best_match += '<div class="progress"> <div class="progress-bar progress-bar-success" role="progressbar" style="width: '
        best_match += str(entity_list[0]['label_confd'] * 100) + '%;" aria-valuemin="0" aria-valuemax="100">'
        best_match += str(entity_list[0]['label_confd'])[:7] + '</div></div>'
        best_match += '<h4><a href="detail.html?title=' + entity_list[0]['label_name'] + '">[查看详细]</a></h4></div></div>'

        ctx['best_match'] = best_match

        other_match = ''
        for i in range(1, len(entity_list)):
            other_match += '<div class="row"> <div class="col-md-5"> <a href="#" class="thumbnail">'
            other_match += '<img src="' + entity_list[i]['image'] + '" height="100%" width="100%"/></a></div>'
            other_match += '<div class="col-md-7"><h4>' + entity_list[i]['label_name'] + '</h4>'
            other_match += '</h5> 置信度：</h5>'
            other_match += '<div class="progress"> <div class="progress-bar progress-bar-info" role="progressbar" style="width: '
            other_match += str(entity_list[i]['label_confd']*100)+'%;" aria-valuemin="0" aria-valuemax="100">'
            other_match += str(entity_list[i]['label_confd'])[:7] +'</div></div></div></div>'

        ctx['other_match'] = other_match

        entity = entity_list[0]['label_name']
        ctx['best_match_title'] = entity
        # 连接数据库
        db = neo_con
        entityRelation = db.getEntityRelationbyEntity(entity)
        if len(entityRelation) == 0:
            # 若数据库中无法找到该实体，则返回数据库中无该实体
            ctx_graph = {'title': '<h1>数据库中暂未添加该实体</h1>'}
            ctx['graph'] = json.dumps(ctx_graph, ensure_ascii=False)
        else:
            # 返回查询结果
            # 将查询结果按照"关系出现次数"的统计结果进行排序
            entityRelation = sortDict(entityRelation)
            ctx['graph'] = json.dumps(entityRelation, ensure_ascii=False)
    return render(request, 'decisions_making.html', ctx)