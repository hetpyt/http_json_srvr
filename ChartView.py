import json
import datetime
from os.path import dirname, join


class ChartView:
    __template_dir = join(dirname(__file__), 'templates')
    __template_one = join(__template_dir, 'chart.html')
    __template_all = join(__template_dir, 'chart_all.html')

    def init_chart(self, chart_name):
        title = ''
        y_title = ''
        if chart_name == 'temp':
            title = 'Temperature'
            y_title = 'Temp (C)'
        if chart_name == 'humi':
            title = 'Humidity'
            y_title = 'Percent (%)'
        if chart_name == 'qfe':
            title = 'QFE'
            y_title = 'Pressure (hPa)'

        return {
            'time': {
                'timezoneOffset': -3 * 60
            },
            'chart': {
                'type': 'spline'
            },
            'title': {
                'text': title
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
                    'text': y_title
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

    def __init__(self, ds, uri=''):
        self.__template = self.__template_one
        self.__container_id = 'container'

        self.__charts = []
        self.__fields = ['date', 'time']
        self.__data_store = ds

        print(uri)
        if uri == 'temp':
            self.__fields.append('temp')
            self.__charts.append({
                'name': "temp",
                'chart': self.init_chart('temp')
            })
        elif uri == 'humi':
            self.__fields.append('humi')
            self.__charts.append({
                'name': "humi",
                'chart': self.init_chart('humi')
            })
        elif uri == 'qfe':
            self.__fields.append('qfe')
            self.__charts.append({
                'name': "qfe",
                'chart': self.init_chart('qfe')
            })
        else:
            self.__template = self.__template_all
            charts = ['temp', 'humi', 'qfe']
            self.__fields += charts
            for chart in charts:
                self.__charts.append({
                    'name': chart,
                    'chart': self.init_chart(chart)
                })

    def render(self):
        data = self.__data_store.query(self.__fields)
        with open(self.__template, 'r') as f:
            template = f.read()
        if len(self.__charts) == 1:
            chart = self.__charts[0]
            return template.replace(
                '%CHART_CONTAINER_ID%', '%s-%s' % (self.__container_id, chart['name'])
            ).replace(
                '%CHART_DATA%',
                json.dumps(self.__chart_data(chart['chart'], data))
            )
        else:
            chart_index = 0
            for chart in self.__charts:
                template = template.replace(
                    '%CHART_DATA_' + chart['name'].upper() + '%',
                    json.dumps(self.__chart_data(chart['chart'], data, chart_index))
                )
                chart_index += 1
            return template

    def __prepare_rows(self, rows, row_num=2):
        result = []
        for row in rows:
            # time in db in UTC
            result.append((
                int(datetime.datetime.fromisoformat('%s %s+00:00' % (row[0], row[1])).timestamp() * 1000),
                row[row_num]))
        return result

    def __chart_data(self, chart, data, chart_num=0):
        for node in data.keys():
            s = {}
            s['name'] = 'node #' + node
            s['data'] = self.__prepare_rows(data[node].rows, chart_num + 2)
            chart['series'].append(s)
        return chart
