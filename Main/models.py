from django.db import models

class FAQ(models.Model):
    question = models.CharField(blank = True, max_length=100,verbose_name = "Question")
    answer = models.CharField(blank = True, max_length=1000,verbose_name = "Answer")

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return f'{self.question}'

class WhatWeDo(models.Model):
    eventNo = models.CharField(verbose_name = "Serial Number", max_length = 2, default = "99")
    eventName = models.CharField(verbose_name = "Name", max_length = 50)
    eventDescription = models.TextField(verbose_name = "Event Description")
    eventCategory = models.CharField(verbose_name = "Avenue", choices = (("1","Professional Development"),("2","Community Service"),("3","International Service")), max_length = 2, default="0")
    eventInstagramPost = models.TextField(verbose_name = "Instagram Post")
    eventVisibility = models.BooleanField(verbose_name = "Status", default = True)

    class Meta:
        verbose_name = 'WhatWeDo'
        verbose_name_plural = 'WhatWeDos'

    def __str__(self):
        return f'{self.eventName}'

