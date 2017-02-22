import vk

vksession = vk.Session()
vkapi = vk.API(vksession)

# [{u'first_name': u'\u0412\u0438\u043a\u0442\u043e\u0440\u0438\u044f',
#   u'has_mobile': 1,
#   u'hidden': 1,
#   u'last_name': u'\u041a\u0443\u0431\u0438\u0446\u043a\u0430\u044f',
#   u'last_seen': {u'platform': 2, u'time': 1476905330},
#   u'online': 0,
#   u'uid': 5746378}]


def query_users(user_ids):
    """
    takes list of user_ids or screen_names (can be mixed)
    returns list of standart VKAPI User objects"""
    return vkapi.users.get(user_ids=user_ids, fields="online,last_seen,has_mobile")


def get_photo(user_ids):
    return vkapi.users.get(user_ids=user_ids, fields="photo_medium")
