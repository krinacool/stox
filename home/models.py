from django.db import models

# Create your models here.
class News(models.Model):
   id=models.AutoField(primary_key=True)
   title = models.CharField(max_length=100)
   content = models.TextField()
   link = models.CharField(max_length=250,default='#')
   datetime = models.DateField(auto_now_add=True)
   class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
   def __str__(self):
      return self.title
   
class CA(models.Model):
   id=models.AutoField(primary_key=True)
   title = models.CharField(max_length=100)
   content = models.TextField()
   link = models.CharField(max_length=250,default='#')
   datetime = models.DateField(auto_now_add=True)
   class Meta:
        verbose_name = "CA"
        verbose_name_plural = "CA"
   def __str__(self):
      return self.title
   
class ExploreVideos(models.Model):
   video_url = models.URLField(blank=True)
   class Meta:
        verbose_name = "Explore Video"
        verbose_name_plural = "Explore Videos"
   def __str__(self):
      return self.video_url