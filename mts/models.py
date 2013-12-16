from django.db import models
from django.db.models.aggregates import Sum, Count, Avg

''' time - time of record
    data_type - [Call, Sms, Internet]
    direction - [Incoming, Oncoming, Null {}]
    number - [phone number - {str}]
    duration - [time in seconds or size in Kb {int}]
    operator - [Velcom, MTS, Life, State, Unknown]
'''


class Operator(models.Model):
    name = models.CharField(max_length=10, null=False)
    code = models.CharField(max_length=1, null=True, blank=True)

    def __unicode__(self):
        return self.name


FORMAT_TIME = '%d.%m.%Y %H:%M:%S'
DURATION_TIME = '%M:%S'
INCOMING = 'In'
OUTGOING = 'Out'
DIRECTION_CHOICES = (
    (INCOMING, 'Incoming'),
    (OUTGOING, 'Outgoing'),
)
SMS = 'Sms'
CALL = 'Call'
INTERNET = 'Internet'
USSD = 'Ussd'
DATA_CHOICES = (
    (SMS, 'Sms'),
    (CALL, 'Call'),
    (INTERNET, 'Internet'),
    (USSD, 'Ussd'),
)


class DataRecord(models.Model):
    time = models.DateTimeField(null=False)
    data_type = models.CharField(choices=DATA_CHOICES, max_length=20, blank=True, null=True)
    direction = models.CharField(choices=DIRECTION_CHOICES, default=OUTGOING, max_length=20)
    number = models.CharField(max_length=18, blank=True, null=True)
    duration = models.IntegerField(null=False)
    operator = models.ForeignKey(Operator, blank=True, null=True)

    @staticmethod
    def get_call_volume(direction=OUTGOING, operator_name='Unknown'):
        operator = Operator.objects.filter(name=operator_name)
        total_call_time = DataRecord.objects.filter(data_type=CALL, direction=direction).aggregate(Sum('duration')).values()[0]
        eval_call_time = \
            DataRecord.objects.filter(data_type=CALL, direction=direction, operator=operator).aggregate(Sum('duration')).values()[0]
        return eval_call_time*100/total_call_time

    @staticmethod
    def get_top_caller(count, direction=OUTGOING):
        return DataRecord.objects \
                   .filter(data_type=CALL, direction=direction) \
                   .values('number') \
                   .annotate(time=Sum('duration')) \
                   .annotate(count=Count('number')) \
                   .annotate(average_time=Avg('duration')) \
                   .order_by('-time')[:count]

    @staticmethod
    def get_top_calls_info(count, attribute, direction):
        result = {'keys': [], 'values': []}
        for item in DataRecord.get_top_caller(count, direction=direction):
            n = item['number']
            result['keys'].append("%s(%s)%s-%s-%s" % (n[:-9], n[-9:-7], n[-7:-4], n[-4:-2], n[-2:]))
            result['values'].append(item[attribute])
        return result
