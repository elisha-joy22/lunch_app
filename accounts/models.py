from django.db import models


class CustomUser(models.Model):
    slack_id = models.CharField(max_length=100,unique=True, db_index=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.name