from django.db import models


# Create your models here.


class Student(models.Model):
    gender_choices = (
        (0, "male"),
        (1, "female"),
        (2, "other"),
    )
    name = models.CharField(max_length=20)
    gender = models.SmallIntegerField(choices=gender_choices, default=0)
    phone = models.CharField(max_length=11, null=True, blank=True)

    class Meta:
        db_table = "bz_student"
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
