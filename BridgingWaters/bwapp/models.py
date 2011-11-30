from django.db import models

class NewsUpdate(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=30) #TODO: Link to admin user
    
    def __unicode__(self):
        return self.title
   
