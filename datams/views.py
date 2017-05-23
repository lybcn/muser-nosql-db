# coding=utf-8
import json

from cassandra import ConsistencyLevel
from django.shortcuts import render, render_to_response

# Create your views here.
from django.http import HttpResponse
import datetime
from cassandra.cluster import Cluster
from cassandra.query import dict_factory, SimpleStatement


def current_datetime(request):
    # 计算当前日期和时间，并以 datetime.datetime 对象的形式保存为局部变量 now
    now = datetime.datetime.now()

    # 构建Html响应，使用now替换占位符%s
    html = "<html><body>It is now %s.</body></html>" % now

    # 返回一个包含所生成响应的HttpResponse对象
    return HttpResponse(html)


def homePage(request):
    return HttpResponse("this is homepage")


def indexPage(request):
    list = [{id: 1, 'name': '李鹏程'}, {id: 2, 'role': '管理员'}]
    return render_to_response('index.html', {'userInfo': list})


def query(request):
    try:
        cluster = Cluster(['222.197.221.227', '222.197.221.225', '222.197.221.233'])
        session = cluster.connect('muserdatadb')
        session.row_factory = dict_factory
        query = 'select time,filename,frequence,kind,offset,polarization from muserdata limit 5'
        sql = SimpleStatement(query, consistency_level=ConsistencyLevel.LOCAL_ONE)
        rows = session.execute(sql)
        list = []
        for row in rows:
            list.append(row)
        final_result = {'total': len(list), "row": list}
        json_string = json.dumps(final_result)
        html = "<html><body>%s</body></html>" % json_string
    except Exception as err:
        html = "<html><body>%s</body></html>" % err
    finally:
        return HttpResponse(html)
