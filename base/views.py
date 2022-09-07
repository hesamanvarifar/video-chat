from sqlite3 import Time
import random
import time
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from agora_token_builder import RtcTokenBuilder

from .models import RoomMember


def get_token(request):
    appId = "daaa4cb155ea49309896e3baf819202b"
    appCertificate = "922bca882c384f278dc06256ff6afdae"
    channelName = request.GET.get("channel")
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs
    )
    return JsonResponse({"token": token, "uid": uid}, safe=False)


def lobby(request):
    return render(request, "base/lobby.html")


def room(request):
    return render(request, "base/room.html")


@csrf_exempt
def create_user(request):

    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data["name"], uid=data["UID"], room_name=data["room_name"]
    )
    return JsonResponse({"name": data["name"]}, safe=False)


def get_member(request):
    uid = request.GET.get("uid")
    room_name = request.GET.get("room_name")

    member = RoomMember.objects.get(uid=uid, room_name=room_name)
    name = member.name
    return JsonResponse({"name": name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)