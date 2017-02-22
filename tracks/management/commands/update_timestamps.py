from django.core.management.base import BaseCommand, CommandError
from tracks.models import User, Timestamp
from datetime import datetime
from tracks.vk_api_helper import query_users
from django.db import transaction


class Command(BaseCommand):
    help = "Creates new Timestamp for every User in database"

    @transaction.atomic
    def handle(self, *args, **options):
        try:
            # TODO: refactor this to bulk updates
            users = User.objects.filter(tracking=True)
            if users:
                vk_users = query_users([u.uid for u in users])

                for vk_user in vk_users:
                    db_user = User.objects.filter(uid=vk_user["uid"])
                    ts = Timestamp(
                        last_seen_time=datetime.fromtimestamp(vk_user["last_seen"]["time"]),
                        last_seen_platform=vk_user["last_seen"]["platform"]
                            if vk_user["last_seen"].get("platform") is not None else 0,
                        user=db_user.get(),
                        online=vk_user["online"],
                        online_mobile=vk_user.get("online_mobile") if vk_user.get("online_mobile") is not None else False,
                        created_at=datetime.now()
                    )
                    ts.save()

                    db_user_get = db_user.get()
                    db_user_get.last_update = ts.created_at
                    db_user_get.save()

                    #self.stdout.write('Successfully updated user with id %s' % vk_user["uid"])

        except Exception as e:
            raise CommandError("%s" % e.message)
