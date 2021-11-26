import json
import datetime


class ChartView:
    __template = 'templates/chart.html'

    def __init__(self, ds, uri=''):
        self.__chart = {
            'time': {
                'timezoneOffset': -3 * 60
            },
            'chart': {
                'type': 'spline'
            },
            'title': {
                'text': 'temperature'
            },
            'xAxis': {
                'type': 'datetime',
                'dateTimeLabelFormats': {
                    'day': '%e. %b',
                },
                'title': {
                    'text': 'Date'
                }
            },
            'yAxis': {
                'title': {
                    'text': 'date'
                }
            },
            'series': [],
            'responsive': {
                'rules': [{
                    'condition': {
                        'maxWidth': 500
                    },
                    'chartOptions': {
                        'plotOptions': {
                            'series': {
                                'marker': {
                                   'radius': 2.5
                                }
                            }
                        }
                    }
                }]
            }
        }
        self.__data_store = ds
        #if uri == 'temp':
        self.__title = 'Temperature'
        self.__data = ds.get_temp()

    def render(self):
        with open(self.__template, 'r') as f:
            template = f.read()
        return template.replace('%CHART_CONTAINER_ID%', 'container-temp').replace('%CHART_DATA%', json.dumps(self.chart_data()))

    def prepare_rows(self, rows):
        result = []
        for row in rows:
            result.append((int(datetime.datetime.fromisoformat(row[0]).timestamp() * 1000), row[1]))
        return result

    def chart_data(self):
        self.__chart['title']['text'] = 'temp'
        self.__chart['yAxis']['title']['text'] = 'temp'
        for node in self.__data.keys():
            s = {}
            s['name'] = 'node #' + node
            s['data'] = self.prepare_rows(self.__data[node].rows)
            self.__chart['series'].append(s)
        return self.__chart
