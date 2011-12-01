from django.db import models

class NewsUpdate(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=30) #TODO: Link to admin user
    
    def __unicode__(self):
        return self.title
    
#--------------------------------------

 
class CodeRegion(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.value

class CodeElevation(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.value

class CodeTopography(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.value

class CodeProjType(models.Model):
    code = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.value
    
class Location(models.Model):
    country = models.CharField(max_length=30)
    name = models.CharField(max_length=60)
    latitude = models.FloatField()
    longitude = models.FloatField()
    region = models.ForeignKey(CodeRegion)
    elevation = models.ForeignKey(CodeElevation)
    topography = models.ForeignKey(CodeTopography)
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.country)
        
class Project(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    goal = models.CharField(max_length=768)
    proj_mgmt = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    #keywords
    #owner = User
    proj_types = models.ManyToManyField(CodeProjType, null=True)
    #organizations
    #proj_contacts
    #hum_res_contacts
    location = models.ForeignKey(Location)
    #climate
    #comm_info
    #geo_cond
    #material_res
    #infra_res
    #natural_res
    #retail_res
    #transpo_res
    #funding_sources
    
    def __unicode__(self):
        return self.title
   
class FeaturedProject(models.Model):
    project = models.ForeignKey(Project)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.project.title

