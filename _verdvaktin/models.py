import re
from django.db import models

class Cpu(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    regex = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.name
    def get_group_from_regex(name):
        for cpu in Cpu.objects.all():
            if(bool(re.search(cpu.regex, name))):
                return cpu
        return Cpu.objects.get(id="None")
