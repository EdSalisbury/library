from django.db import models

class Amazon(models.Model):
    access_key = models.CharField("Access Key", max_length = 20)
    secret_key = models.CharField("Secret Key", max_length = 40)
    assoc_tag = models.CharField("Associate ID", max_length = 20)

    def __unicode__(self):
        return self.access_key

    class Meta:
        verbose_name = "Amazon Key"
