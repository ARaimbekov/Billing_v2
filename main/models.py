from django.db import models
from django.contrib.postgres.fields import BigIntegerRangeField


# Create your models here.
class CallDetailRecord(models.Model):
    """ Основной класс первоначальных CDR """
    outbound_cid = models.fields.CharField(
        max_length=80,
        default='',
    )
    src = models.CharField(max_length=80)
    dst = models.fields.CharField(
        max_length=80,
    )
    diversion = models.fields.CharField(
        max_length=64,
        default='',
    )
    channel = models.fields.CharField(max_length=80)
    dst_channel = models.fields.CharField(
        max_length=80,
    )
    start = models.fields.DateTimeField()
    answer = models.fields.DateTimeField(null=True)
    end = models.fields.DateTimeField(null=True)
    duration = models.fields.IntegerField(default=0)
    billsec = models.fields.IntegerField(default=0)
    disposition = models.fields.CharField(max_length=80)
    uniquie_id = models.fields.CharField(max_length=80)
    pbx = models.fields.CharField(max_length=80, default='')
    id = models.fields.UUIDField(primary_key=True)

    class Meta:
        verbose_name = 'Изначальный Список Звонков'
        verbose_name_plural = verbose_name


class CountedCallDetailRecord(models.Model):
    """ Подсчитанные CDR с работником и ценой """
    outbound_cid = models.fields.CharField(
        max_length=80,
        default='',
    )
    src = models.CharField(max_length=80)
    dst = models.fields.CharField(
        max_length=80,
    )
    diversion = models.fields.CharField(
        max_length=64,
        default='',
    )
    channel = models.fields.CharField(max_length=80)
    dst_channel = models.fields.CharField(
        max_length=80,
    )
    start = models.fields.DateTimeField()
    answer = models.fields.DateTimeField(null=True)
    end = models.fields.DateTimeField(null=True)
    duration = models.fields.IntegerField(default=0)
    billsec = models.fields.IntegerField(default=0)
    disposition = models.fields.CharField(max_length=80)
    uniquie_id = models.fields.CharField(max_length=80)
    pbx = models.fields.CharField(max_length=80, default='')
    id = models.fields.UUIDField(primary_key=True)
    price = models.fields.FloatField(default=0.0)

    class Meta:
        verbose_name = 'Список Звонков'
        verbose_name_plural = verbose_name
        unique_together = ['uniquie_id', 'pbx']


class Tarif(models.Model):
    """ Основной класс тарифов операторов """
    code = BigIntegerRangeField(blank=True, null=True)


class Company(models.Model):
    """ Компании предприятия """
    name = models.CharField(max_length=256, verbose_name='Имя компании')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компании'
        verbose_name_plural = verbose_name


class Department(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='Компания'
    )
    name = models.CharField(max_length=256, verbose_name='Имя отдела')

    def __str__(self):
        return f'{self.company.name}: {self.name}'

    class Meta:
        verbose_name = 'Отделы'
        verbose_name_plural = verbose_name


class Employee(models.Model):
    """ Сотрудники предприятия """
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name='Отдел'
    )
    surname = models.fields.CharField(
        max_length=64,
        verbose_name='Фамилия'
    )
    name = models.fields.CharField(
        max_length=64,
        verbose_name='Имя'
    )
    last_name = models.fields.CharField(
        max_length=64,
        verbose_name='Отчество'
    )
    position = models.fields.CharField(
        max_length=512,
        verbose_name='Должность'
    )
    work_number = models.fields.CharField(
        max_length=32,
        #        unique=null,
        verbose_name='Рабочий телефон (Asterisk код)'
    )
    additional_number = models.fields.CharField(
        max_length=32,
        verbose_name='Дополнительный номер'
    )

    @property
    def full_name(self) -> str:
        return f'{self.surname} {self.name} {self.last_name}'

    def __str__(self):
        return (
            f'{self.surname} {self.name}, {self.department.company.name},'
            f' {self.department.name}, {self.position}'
        )

    def __lt__(self, other):
        return self.full_name < other.full_name

    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = verbose_name
