from django.db import models


class Puppy(models.Model):
    """
    Puppy Model
    Defines the attributes of a puppy
    """
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    breed = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    # 创建的时候将时间更新新为当前时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 每次save的时候时间更新为当前时间
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    def get_breed(self):
        return self.name + ' belongs to ' + self.breed + ' breed.'

    def __repr__(self):
        return self.name + ' is added.'