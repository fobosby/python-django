import re
from django.db import transaction
from django.utils.datetime_safe import datetime
from lxml import etree
from mts.models import DataRecord, FORMAT_TIME, DURATION_TIME, INCOMING, OUTGOING, CALL, SMS, INTERNET, Operator


'''
Incoming call from Velcom example
<c>
    <d>11.10.2013 19:14:20</d>
    <n><--V:375296401998</n>
    <zp/>
    <zv/>
    <s/>
    <a/>
    <du>1:13</du>
    <c>0</c>
    <bd>11.10.2013 19:20:17</bd>
    <dup>2:00</dup>
    <cur>974</cur>
</c>

Incoming sms from life
<c>
    <d>11.10.2013 10:33:28</d>
    <n><--L:375259092003</n>
    <zp/>
    <zv/>
    <s>sms i</s>
    <a/>
    <du>1</du>
    <c>0</c>
    <bd>11.10.2013 10:37:48</bd>
    <dup>1</dup>
    <cur>974</cur>
</c>

Internet data
<c>
    <d>11.10.2013 10:36:21</d>
    <n>INTERNET</n>
    <zp/>
    <zv/>
    <a/>
    <du>16Kb</du>
    <c>0</c>
    <bd>11.10.2013 11:04:40</bd>
    <dup>16Kb</dup>
    <cur>974</cur>
</c>

'''

NUMBER_PATTERN = r'\d+'
OPERATOR_PATTERN = '%s{1}'


def file_handler(xml_file):
    auto_commit_status = transaction.get_autocommit()
    transaction.set_autocommit(False)
    value = xml_file.read()
    tree = etree.fromstring(value)
    operators = {}
    for item in Operator.objects.all():
        operators[item.code] = item
    result = []
    for item in tree.xpath('//td/c'):
        get_value = lambda xpath: item.xpath(xpath)[0].text
        data_record = DataRecord()
        data_record.time = datetime.strptime(get_value('./d'), FORMAT_TIME)
        data_type = get_value('./s')
        data_type = data_type if data_type is not None else ''
        duration = get_value('./du')
        if 'INTERNET' in get_value('./n'):
            data_record.data_type = INTERNET
            data_record.duration = duration[:-2]  # Remove 'Kb' from string
        else:
            data_record.operator = operators.get('U')
            source = get_value('./n')
            for operator_code in operators.keys():
                if operator_code in source:
                    data_record.operator = operators.get(operator_code)
                    break
            data_record.number = re.findall(NUMBER_PATTERN, get_value('./n'))[0]
            data_record.direction = INCOMING if '<--' in get_value('./n') else OUTGOING
            if 'sms' in data_type:
                data_record.data_type = SMS
                data_record.duration = duration
            elif 'ussd' in data_type:
                continue
            else:
                data_record.data_type = CALL
                call_duration = datetime.strptime(duration, DURATION_TIME)
                data_record.duration = call_duration.minute * 60 + call_duration.second
        data_record.save()
        result.append(data_record)
    transaction.commit()
    transaction.set_autocommit(auto_commit_status)
    return result
