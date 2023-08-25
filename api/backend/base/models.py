from django.db import models

class Ping(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    dc_user = models.BigIntegerField(primary_key=False, null=False, blank=False, verbose_name="DC ID of user")
    ping_count = models.IntegerField(primary_key=False, null=False, blank=False, default=0, verbose_name="Number of pings")
    last_ping = models.DateTimeField(auto_now=True, verbose_name="Last ping")

    def __str__(self):
        return f'{self.dc_user} - {self.ping_count}'
