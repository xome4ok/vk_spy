import json
from django.http import HttpResponse
from .models import Timestamp, User
from django.shortcuts import render
from vk_api_helper import query_users, get_photo
from datetime import datetime
from uuid import uuid4
from urlparse import urlparse


def user_track_json(request, user_id):
    user = User.objects.filter(uid=user_id)
    if user:
        user = user.get()
        track = [
            {'last_seen_time': ts.last_seen_time.isoformat(),
                'last_seen_platform': ts.last_seen_platform,
                'online': ts.online,
                'online_mobile': ts.online_mobile,
                'created_at': ts.created_at.isoformat()} for ts
            in Timestamp.objects.filter(user=user).order_by("created_at")
            ]

        track_changes = 0
        online_count = sum((1 for t in track if t['online']))
        mobile_count = sum(1 for t in track if t['online_mobile'])
        platform_stats = [{Timestamp.PLATFORMS[i-1][1]:
                               sum(1 for t in track if t['last_seen_platform'] == i)}
                          for i in range(1, 8)] # platform name : number of total visits tracked

        return HttpResponse(json.dumps({'result': True,
                                        'track': track,
                                        'count': len(track),
                                        'online_count': online_count,
                                        'mobile_count': mobile_count,
                                        'platform_stats': platform_stats,
                                        'track_changes': track_changes}),
                            content_type='application/json')

    else:
        return HttpResponse(json.dumps({'result': False, 'message': 'User not found.', 'track': None}),
                            content_type='application/json')


def user_start_tracking_by_page_address(request):
    link = request.POST.get("link")
    id_or_screenname = urlparse(link).path.strip('/')
    if id_or_screenname:
        from vk.exceptions import VkAPIError
        try:
            vk_query = query_users(id_or_screenname)
            uid = vk_query[0]["uid"]
            return user_start_tracking(request, uid)
        except VkAPIError as e:
            return users_view(request)
    else:
        return users_view(request)


def user_start_tracking(request, user_id):
    try:
        vk_user = query_users(user_id)[0]
        if not User.objects.filter(uid=vk_user["uid"]):
            secret = uuid4().get_hex()
            u = User(
                first_name=vk_user["first_name"],
                last_name=vk_user["last_name"],
                has_mobile=vk_user["has_mobile"],
                uid=vk_user["uid"],
                last_update=datetime.now(),
                secret=secret
            )
            u.save()

            return HttpResponse(json.dumps(
                {'result': True, 'secret': secret}),
                content_type='application/json')
        else:
            return HttpResponse(json.dumps(
                {'result': False, 'message': "This user is already tracked."}),
                content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({'result': False, 'message': e.message, 'response': vk_user}),
                            content_type='application/json')


def user_stop_tracking(request, user_id):
    user = User.objects.filter(uid=user_id)
    if user:
        user = user.get()
        secret = request.POST.get('secret')
        if secret == user.secret:
            user.tracking = False
            user.save()
            return render(request, "tracks/stop_result.html", {'result': True, 'user': user})
        else:
            print 'user secret: ', user.secret, '; you entered: ', request.POST.get('secret')
            return render(request, "tracks/stop_result.html", {'result': False, 'message': 'Invalid secret.'})
    else:
        return render(request, "tracks/stop_result.html", {'result': False, 'message': 'User is not found.'})


def secret_form(request, user_id):
    user = User.objects.filter(uid=user_id)
    if user:
        user = user.get()
        context = {'user': user}
        return render(request, "tracks/secret_form.html", context)
    else:
        return render(request, "tracks/secret_form.html")


def user_info_view(request, user_id):
    """should include track info. like it's advanced view with every piece of info included"""
    user = User.objects.filter(uid=user_id)
    if user:
        user = user.get()
        track = Timestamp.objects.filter(user=user).order_by("-created_at")
        context = {'user': user, 'track': track, "given_uid": user_id, 'photo': get_photo(user.uid)[0].get("photo_medium"),
                   'track_started': track.last().created_at}
        return render(request, "tracks/user_info.html", context)
    else:
        context = {'user': None, 'track': None, 'given_uid': user_id}
        return render(request, "tracks/user_info.html", context)


def users_view(request):
    users = list(User.objects.all())
    context = {'users': users}
    return render(request, "tracks/users.html", context)


def index(request):
    return users_view(request)