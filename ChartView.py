import json


class ChartView:
    __series = {
        'name': '',
        'data': []
    }
    __chart = {
        'title': {
            'text': 'Fruit Consumption'
        },
        'xAxis': {
            'categories': []
        },
        'series': []
    }
    __template = 'templates/chart.html'

    def __init__(self, data):
        self.__chart['title']['text'] = 'temp'
        self.__chart['xAxis']['categories'] = data['date']
        s1 = self.__series
        s1['name'] = 'temp'
        s1['data'] = data['temp']
        self.__chart['series'].append(s1)
        pass

    def render(self):
        with open(self.__template, 'r') as f:
            template = f.read()
        return template.replace('%CHART_CONTAINER_ID%', 'chart').replace('%CHART_DATA%', json.dumps(self.__chart))

    def build_data(self):
        pass