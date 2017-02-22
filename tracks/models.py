from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    has_mobile = models.BooleanField()
    uid = models.IntegerField()
    last_update = models.DateTimeField()
    secret = models.CharField(default="00000000000000000000000000000000", max_length=32)
    tracking = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.uid)


class Timestamp(models.Model):
    PLATFORMS = ((1, "mobile version"),
                 (2, "iphone app"),
                 (3, "ipad app"),
                 (4, "android app"),
                 (5, "winphone app"),
                 (6, "win8 app"),
                 (7, "full version"))

    last_seen_time = models.DateTimeField()
    last_seen_platform = models.IntegerField(choices=PLATFORMS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    online = models.BooleanField()
    online_mobile = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True)

    def __unicode__(self):
        return str(self.created_at) + " - " + str(self.user.uid)
