from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Language


User = get_user_model() # table of user
class Audio(models.Model):
    """
            class des Audios
    """
    path=models.CharField(max_length=250, unique=True)
    name=models.CharField(max_length=250, unique=True)
    language=models.ForeignKey(Language, related_name="music", on_delete=models.DO_NOTHING)
    creation_date = models.DateTimeField(auto_now_add=True)
    annotation = models.ManyToManyField(User, through="Annotation")
    numAnnotate = models.IntegerField(default=0) 
    
    class Meta:
        ordering = ['-creation_date', 'path', 'language']
    
    def __str__(self) -> str:
        return  self.path


    def save(self,*args, **kwargs):
        return super(Audio, self).save(*args, **kwargs)

def last_video_save():
    return Video.objects.all().count()

class Video(models.Model):
    """
            class des videos
    """
    name=models.CharField(max_length=250, unique=True)
    path=models.CharField(max_length=250, unique=True)
    language=models.ForeignKey(Language, related_name="video", on_delete=models.DO_NOTHING)
    creation_date = models.DateTimeField(auto_now_add=True)
    annotation = models.ManyToManyField(User, through="AnnotationVideo")
    numAnnotate = models.IntegerField(default=0) 

    class Meta:
        ordering = ['-creation_date', 'name', 'path', 'language']
    
    def __str__(self) -> str:
        return  self.name


    def save(self,*args, **kwargs):
        return super(Video, self).save(*args, **kwargs)

class Emotion(models.Model):
    """
        emotions list
    """
    name = models.CharField(max_length=250, unique=True)
    emoji=models.CharField(max_length=250, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-creation_date", "name"]
        
    def __str__(self) -> str:
        return self.name


class AnnotationVideo(models.Model):
    """
            user video annotation
    """
    emotion=models.ForeignKey(Emotion,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="annotation_video", on_delete=models.DO_NOTHING)
    Video = models.ForeignKey(Video, related_name="annotations", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-creation_date']
    
    def __str__(self) -> str:
        return f'{self.emotion.name}'

class Annotation(models.Model):
    """
            user annotation
    """
    emotion=models.ForeignKey(Emotion,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="annotations", on_delete=models.DO_NOTHING)
    audio = models.ForeignKey(Audio, related_name="annotations", on_delete=models.CASCADE)

    class Meta:
        ordering = ['-creation_date']
    
    def __str__(self) -> str:
        return f'{self.emotion.name}'

class AudioResultAnnotation(models.Model):
    audio      = models.ForeignKey(Audio, related_name="note_finale", on_delete=models.CASCADE)
    audio_name = models.CharField( max_length=250)
    note_name  = models.CharField(max_length=250)
    note_emoji = models.CharField(max_length=250)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.audio_name

    def save(self,*args, **kwargs):
        self.audio_name =  self.audio.name
        
        return super(AudioResultAnnotation, self).save(*args, **kwargs)