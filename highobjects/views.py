import json
import os
from datetime import datetime, timedelta
import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
import time
import jwt
from django.http import JsonResponse
from .models import EventsRawMode
from rest_framework.response import Response
from rest_framework.views import APIView
from BAtest import settings


def new_flows_journeys_route(header,flow_id, user_id, payload_url=None, entries_attributes=None):

    params = {
        "assignment": {
            "operation": "route",
            "response_attributes": {
                "entries_attributes": entries_attributes
            }
        },
        "user_id": user_id,
        "webhook": {
            "payload_url": payload_url,
            "subscribed_events": [
                "JourneyStatusEvent"
            ]
        },
    }
    url = settings.URL
    url = '%s/api/v4/yaw/flows/%d/journeys' % (url,flow_id)
    print(url)
    first = requests.request('POST',url=url, json=params,headers=header,verify=False)
    return first.text


# 发起新流程 步骤2 propose
def new_flows_journeys_propose(header,flow_id, user_id, next_vertex_id, entries_attributes=None,
                               next_reviewer_ids=None, duration_thresholds=None):
    params = {
        "assignment": {
            "operation": "propose",
            "next_vertex_id": next_vertex_id,
        },
        "user_id": user_id,
    }
    if next_reviewer_ids:
        params['assignment']['next_reviewer_ids'] = next_reviewer_ids

    if duration_thresholds:
        params['assignment']['duration_thresholds'] = duration_thresholds

    if entries_attributes:
        params['assignment']['response_attributes']['entries_attributes'] = entries_attributes
    url = settings.URL
    url = '%s/api/v4/yaw/flows/%d/journeys' % (url, flow_id)
    second = requests.request('POST', url=url, json=params, headers=header, verify=False)
    return second


# 获取附件信息
def get_attachments_by_id(header,attachments_id):
    # 获取附件信息
    url = settings.URL
    url = '%s/api/v4/attachments/query?ids=%d' % (url,attachments_id)
    print(url)
    info = requests.get(url,headers=header, verify=False)
    return info


# 获取上传文件token
def get_attachments_uptoken(header,user_id):
    # 获取上传文件token
    url = settings.URL
    if user_id:
        url = f"%s/api/v4/attachments/uptoken?purpose=create_responses&user_id={user_id}" % url
    else:
        url = f"%s/api/v4/attachments/uptoken?purpose=create_responses" % url
    r = requests.get(url,headers=header,verify=False)
    return r


def upload_file_by_fileobj(header,save_path,user_id):
    # 上传文件
    r = get_attachments_uptoken(header=header,user_id=user_id)
    r = r.json()
    if r:
        uptoken = r['uptoken']
        upload_url = 'https://up.qbox.me/'
        upload_data = {
            'token': uptoken,
            'x:key': '1593586993541'
        }
        files = {"file": open(save_path, 'rb')}
        result = requests.post(upload_url, upload_data, files=files, verify=False)
        return result.json()

@permission_classes((AllowAny,))
class DataView(APIView):

    def post(self,request):
        app_id = settings.APPID
        app_secret = settings.APPSECRET
        id = settings.ID
        header = ApiApplication(app_id=app_id,app_secret=app_secret,id=id)
        print(header)
        data = request.body
        data = json.loads(data)
        # 将数据存入数据库
        # 创建 EventsRawMode 对象并保存
        event = EventsRawMode()
        for key, value in data.items():
            if hasattr(event, key):
                setattr(event, key, value)
        event.save()
        # 将字符串转换为datetime对象
        original_time = datetime.fromisoformat(data["dateTime"])
        # 添加8小时时差，转换为北京时间的格式
        beijing_time_str = (original_time + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
        print(beijing_time_str)
        # 更新data中的dateTime值
        data["dateTime"] = beijing_time_str
        #获取流程结构信息
        url = settings.URL
        flow_id = settings.gkpw_flow_id
        user_id = settings.gkpw_user_id
        url = '%s/api/v4/yaw/flows/%d' % (url,flow_id)
        processinfo = requests.request('GET', url=url, headers=header, verify=False)
        info = processinfo.text
        info = json.loads(info)
        infodata = []
        for field in info['fields']:
            if field['identity_key'] in data or data['ObjectsThrownDetection']:
                if field['type'] == "Field::File":
                    file_data = {
                        "resourcesContent": data['ObjectsThrownDetection'][0]["Image"]["resourcesContent"],
                        "resourcesContentType": data['ObjectsThrownDetection'][0]['Image']['resourcesContentType']
                    }
                    # 发起GET请求下载图片
                    image_url = file_data["resourcesContent"]
                    # 下载的图片保存在些应用的download images目录下
                    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download images')
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # 获取文件名
                        file_name = image_url.split('/')[-1]
                        save_path = os.path.join(save_dir, file_name)
                        # 保存图片到本地
                        with open(save_path, 'wb') as f:
                            f.write(response.content)
                        qn = upload_file_by_fileobj(header,save_path,user_id)
                        # 处理完成后，删除该图片
                        os.remove(save_path)
                        print(save_path)
                        infodata.append({
                            "field_id": field['id'],
                            "value_id":qn['id'],
                            "value":file_data['resourcesContent']
                        })
                elif field['identity_key'] == 'objectType':
                    infodata.append({
                        "field_id": field['id'],
                        "value": '高空抛物'
                    })
                elif field['identity_key'] in data:
                    infodata.append({
                        "field_id": field['id'],
                        "value": data[field['identity_key']]
                    })
        print(infodata)
        # 第一次调用
        result = new_flows_journeys_route(header,flow_id, user_id,entries_attributes=infodata)
        print(result)
        data = json.loads(result)
        next_vertices = data.get("next_vertices", [])
        first_vertex_id = next_vertices[0].get("id") if next_vertices else None
        print(first_vertex_id)
        # 第二次调用 propose
        result2 = new_flows_journeys_propose(header,flow_id,user_id,next_vertex_id=first_vertex_id)
        print(result2)
        return Response({'msg': '发起流程成功！'})


# 自定义 JSON 序列化方法
def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()





def ApiApplication(app_id,app_secret,id):
    assert app_id, 40001
    assert app_secret, 40001
    assert id, 40001
    timestamp = int(time.time())   #当前时间戳
    print("当前时间戳：", timestamp)
    if app_id and app_secret and id:
        headers = {
          "alg": "HS256",
          "typ": "JWT"
        }
        payload = {
            "namespace_id":id,
            "exp":timestamp+10080   # 过期时间：1周
        }
        print(payload)
        encoded_data = jwt.encode(payload=payload,key=app_secret,headers=headers)
        authorization = "%s:%s" % (app_id, encoded_data.decode())
        print(authorization)
        headers = {
            'Authorization':authorization,
            'Content-Type':"application/json"
        }
        return headers
    else:
        return JsonResponse(40001)