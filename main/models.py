from django.db import models
from django.contrib.postgres.fields import BigIntegerRangeField


# Create your models here.
class CallDetailRecord(models.Model):
    """ Основной класс первоначальных CDR """


class CountedCallDetailRecord(models.Model):
    """ Подсчитанные CDR с работником и ценой """


class Tarif(models.Model):
    """ Основной класс тарифов операторов """
    code = BigIntegerRangeField(blank=True, null=True)


class Employee(models.Model):
    """ Сотрудники предприятия """


class Department(models.Model):
    """ Отделы предприятия """


class Company(models.Model):
    """ Компании предприятия """
