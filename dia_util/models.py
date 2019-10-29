from django.db import models


class Holiday(models.Model):
    SQL_FERIADOS_BETWEEN = ""
    date = models.DateField()
    description = models.CharField(max_length=50)

    class Meta:
        db_table = "Holiday"
        verbose_name = 'Holiday'
        verbose_name_plural = 'Holidays'

    def __str__(self):
        return f"{self.description} - {self.date}"

    @staticmethod
    def select_sql(dates=[]):
        result = Holiday.objects.filter(
            date__range=dates).exclude(date__week_day__in=(0, 7))

        return result
