import json
from django.utils.safestring import SafeString


class BaseChart(object):
    def to_json(self):
        return SafeString(json.dumps(self.__dict__))


class BarChart(BaseChart):
    def __init__(self, values, title='Chart', color='yellow', y_axis_label=''):
        self.chart = {'type': 'bar'}
        self.colors = [color]
        self.title = {'text': title}
        self.xAxis = {'categories': values['keys']}
        self.yAxis = {'title': {'text': y_axis_label}, 'labels': {'overflow': 'justify'}}
        self.plotOptions = {'bar': {'dataLabels': {'enabled': True, 'color': 'white'}}}
        self.legend = {'enabled': False}
        self.credits = {'enabled': False}
        self.series = [{'name': title, 'data': values['values']}]


class AngularChart(BaseChart):
    def __init__(self, value, title='Chart', axis_label=''):
        self.chart = {'type': 'gauge'}
        self.title = {'text': title}
        self.pane = {'startAngle': -150,
                     'endAngle': 150,
                     'background': [{
                                        'backgroundColor': {
                                            'linearGradient': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 1},
                                            'stops': [[0, '#FFF'], [1, '#333']]},
                                        'borderWidth': 0,
                                        'outerRadius': '109%'
                                    }, {'backgroundColor': {
                         'linearGradient': {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 1},
                         'stops': [[0, '#333'], [1, '#FFF']]},
                                        'borderWidth': 1,
                                        'outerRadius': '107%'
                                    }, {'backgroundColor': '#DDD',
                                        'borderWidth': 0,
                                        'outerRadius': '105%',
                                        'innerRadius': '103%'}]
        }
        self.yAxis = {
            'min': 0,
            'max': 100,
            'minorTickInterval': 'auto',
            'minorTickWidth': 1,
            'minorTickLength': 10,
            'minorTickPosition': 'inside',
            'minorTickColor': '#666',
            'tickPixelInterval': 30,
            'tickWidth': 2,
            'tickPosition': 'inside',
            'tickLength': 10,
            'tickColor': '#666',
            'labels': {'step': 2, 'rotation': 'auto'},
            'title': {'text': axis_label},
            'plotBands': [{'from': 0, 'to': 60, 'color': '#55BF3B'},
                          {'from': 60, 'to': 85, 'color': '#DDDF0D'},
                          {'from': 85, 'to': 100, 'color': '#DF5353'}]
        }
        self.series = [{'name': title,
                        'data': [value],
                        'tooltip': {'valueSuffix':  axis_label}}]