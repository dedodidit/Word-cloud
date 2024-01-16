from django.db import models


class WineMask(models.Model):
    name = models.CharField(max_length=255)
    mask_image = models.ImageField(upload_to="wine_masks/")


class WordCloudImage(models.Model):
    image = models.ImageField(upload_to="wordcloud_images/")
