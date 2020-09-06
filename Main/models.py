from django.db import models

class FAQ(models.Model):
    question = models.CharField(blank = True, max_length=100,verbose_name = "Question")
    answer = models.CharField(blank = True, max_length=1000,verbose_name = "Answer")

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return f'{self.question}'
