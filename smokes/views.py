import json
import os
import time

import jwt
import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .models import EventsRawMode
from rest_framework.views import APIView
from BAtest import settings
from django.http import JsonResponse
from highobjects.views  import new_flows_journeys_route, new_flows_journeys_propose,upload_file_by_fileobj
from .models import LocaltionInfo


@permission_classes((AllowAny,))
class DataView(APIView):
    def post(self,request):
        app_id = settings.APPID
        app_secret = settings.APPSECRET
        id = settings.ID
        header = ApiApplication(app_id=app_id, app_secret=app_secret, id=id)
        data = request.body
        data = json.loads(data)
        if data['devicetype'] == 'YG':
            if data['messagetype'] == 2:
                # 匹配位置信息
                device_id = data['imei']
                print(device_id)
                try:
                    record = LocaltionInfo.objects.get(device_id=device_id)
                    data['location'] = record.location
                    # 将数据存入数据库
                    # 创建 EventsRawMode 对象并保存
                    event = EventsRawMode()
                    for key, value in data.items():
                        if hasattr(event, key):
                            setattr(event, key, value)
                    event.save()
                    # 获取流程结构信息
                    url = settings.URL
                    flow_id = settings.yg_flow_id
                    user_id = settings.yg_user_id
                    url = '%s/api/v4/yaw/flows/%d' % (url,flow_id)
                    processinfo = requests.request('GET', url=url, headers=header, verify=False)
                    info = processinfo.text
                    info = json.loads(info)
                    infodata = []
                    for field in info['fields']:
                        value = data.get(field['identity_key'], '无')
                        if field['type'] == "Field::File":
                            file_data = {
                                "resourcesContent": data['ObjectsThrownDetection'][0]["Image"]["resourcesContent"],
                                "resourcesContentType": data['ObjectsThrownDetection'][0]['Image'][
                                    'resourcesContentType']
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
                                qn = upload_file_by_fileobj(header, save_path, user_id)
                                # 处理完成后，删除该图片
                                os.remove(save_path)
                                print(save_path)
                                infodata.append({
                                    "field_id": field['id'],
                                    "value_id": qn['id'],
                                    "value": file_data['resourcesContent']
                                })
                        elif field['identity_key'] == 'devicename':
                            infodata.append({
                                "field_id": field['id'],
                                "value": data['location']
                            })
                        else:
                            infodata.append({
                                "field_id": field['id'],
                                "value": value
                            })
                    print(infodata)
                    # 发起流程
                    # 第一次调用 route
                    result = new_flows_journeys_route(header, flow_id, user_id, entries_attributes=infodata)
                    print(result)
                    # 第二次调用 propose
                    data = json.loads(result)
                    next_vertices = data.get("next_vertices", [])
                    first_vertex_id = next_vertices[0].get("id") if next_vertices else None
                    print(first_vertex_id)
                    result2 = new_flows_journeys_propose(header, flow_id, user_id, next_vertex_id=first_vertex_id)
                    print(result2)
                    return JsonResponse({'msg1': '发起流程成功！'})

                except LocaltionInfo.DoesNotExist:
                    return JsonResponse({'error':"未找到对应的 LocaltionInfo 对象"})
            return JsonResponse({'msg3': '正常数据，不报警！'})
        if data['devicetype'] == 'RD':
            if data['messagetype'] == 2:
                # 将数据存入数据库
                # 创建 EventsRawMode 对象并保存
                event = EventsRawMode()
                for key, value in data.items():
                    if hasattr(event, key):
                        setattr(event, key, value)
                event.save()
                #获取流程结构信息
                url = settings.URL
                flow_id = settings.rd_flow_id
                user_id = settings.rd_user_id
                url = '%s/api/v4/yaw/flows/%d' % (url, flow_id)
                processinfo = requests.request('GET', url=url, headers=header, verify=False)
                info = processinfo.text
                info = json.loads(info)
                infodata = []
                for field in info['fields']:
                    value = data.get(field['identity_key'], '无')
                    if field['type'] == "Field::File":
                        file_data = {
                            "resourcesContent": data['ObjectsThrownDetection'][0]["Image"]["resourcesContent"],
                            "resourcesContentType": data['ObjectsThrownDetection'][0]['Image'][
                                'resourcesContentType']
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
                            qn = upload_file_by_fileobj(header, save_path, user_id)
                            # 处理完成后，删除该图片
                            os.remove(save_path)
                            print(save_path)
                            infodata.append({
                                "field_id": field['id'],
                                "value_id": qn['id'],
                                "value": file_data['resourcesContent']
                            })
                    elif field['identity_key'] == 'devicename':
                        infodata.append({
                            "field_id": field['id'],
                            "value": data['location']
                        })
                    else:
                        infodata.append({
                            "field_id": field['id'],
                            "value": value
                        })
                print(infodata)
                # 发起流程
                # 第一次调用 route
                result = new_flows_journeys_route(header, flow_id, user_id, entries_attributes=infodata)
                print(result)
                # 第二次调用 propose
                data = json.loads(result)
                next_vertices = data.get("next_vertices", [])
                first_vertex_id = next_vertices[0].get("id") if next_vertices else None
                print(first_vertex_id)
                result2 = new_flows_journeys_propose(header, flow_id, user_id, next_vertex_id=first_vertex_id)
                print(result2)
                return JsonResponse({'msg1': '发起流程成功！'})
        return JsonResponse({"msg4": '数据不是烟感或红外，拒绝接收！'})


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


