from django.db import models


class Img(models.Model):
    image = models.ImageField(upload_to='media/', default="https://goo.su/swyUm5")
