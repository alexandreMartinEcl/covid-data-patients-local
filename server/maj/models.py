from django.db import models
import datetime


class MAJ(models.Model):
    description = models.CharField(max_length=1000)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.date.strftime("%m-%d-%Y") + " - " +\
            self.description
