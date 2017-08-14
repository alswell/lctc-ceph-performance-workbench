import urllib
import json
from settings import HOST
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def get_data_by_url(url):
    sock = urllib.urlopen(url)
    data = sock.read()
    sock.close()
    return json.loads(data)


def get_data(res, id=None):
    if id is not None:
        res += "/%s/" % id
    url = HOST + res
    return get_data_by_url(url)


def parse_data(data):
    all_data = {}
    for d in data:
        for k, v in d.items():
            try:
                all_data[k].append(v)
            except KeyError:
                all_data[k] = []
                all_data[k].append(v)
    return all_data


class FormatTime(object):
    def __init__(self, time_array):
        self.time_array = time_array

    def format_date(self, x, pos=None):
        if x < 0 or x >= len(self.time_array):
            return x
        if pos is None:
            return x

        if x - int(x) == 0:
            return self.time_array[int(x)]
        else:
            return ""


def plot_all(all_data, data_to_plot, x_label=None):
    for key, value in all_data.items():
        if value:
            plot_time_y(value, data_to_plot[key], x_label)
    plt.show()


def plot_time_y(all_data, data_to_plot, x_label, y_label='rate'):
    plt.figure()

    if len(all_data) % 2 == 0:
        column_num = 2
    else:
        column_num = 1
    base = len(all_data) / column_num * 100 + 10 * column_num

    i = 0
    items = all_data.items()
    items.sort()
    for key, value in items:
        i += 1
        plt.subplot(base + i)
        plt.title(key)
        plt.ylabel(y_label)
        for k, v in data_to_plot.items():
            if v['need_plot'].get() == 1:
                if isinstance(value[k], dict):
                    x = [index for index in range(len(value[x_label])) if value[k].get(value[x_label][index])]
                    y = [value[k].get(value[x_label][index]) for index in range(len(value[x_label])) if value[k].get(value[x_label][index])]
                    plt.plot(x, y, v['legend'], label=k)
                else:
                    plt.plot(range(len(value[k])), value[k], v['legend'], label=k)

        if x_label:
            plt.xticks(range(len(value[x_label])), value[x_label], horizontalalignment='right', rotation=30, fontsize='small')
        #     fmt = FormatTime(value[x_label])
        #     ax = plt.gca()
        #     ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt.format_date))
        plt.legend()
