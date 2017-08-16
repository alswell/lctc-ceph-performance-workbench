import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


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
    # plt.savefig('test.png', dpi=160)
    plt.show()


def plot_time_y(all_data, data_to_plot, x_label, y_label='rate'):
    plt.figure()

    len_all_data = len(all_data)
    if len_all_data % 6 == 0 and len_all_data > 20:
        column_num = 6
    elif len_all_data % 5 == 0 and len_all_data > 20:
        column_num = 5
    elif len_all_data % 4 == 0 and len_all_data > 20:
        column_num = 4
    elif len_all_data % 3 == 0 and len_all_data > 20:
        column_num = 3
    elif len_all_data % 2 == 0 and len_all_data > 3:
        column_num = 2
    else:
        column_num = 1
    i = 0
    items = all_data.items()
    items.sort()
    for key, value in items:
        i += 1
        plt.subplot(len_all_data / column_num, column_num, i)
        plt.title(key)
        plt.ylabel(y_label)
        for k, v in data_to_plot.items():
            if v['need_plot'].get() == 1:
                if isinstance(value[k], dict):
                    x = [index for index in range(len(value[x_label])) if value[k].get(value[x_label][index])]
                    # y = [value[k].get(value[x_label][index]) for index in range(len(value[x_label])) if value[k].get(value[x_label][index])]
                    y = [value[k].get(value[x_label][index]) for index in x]
                    plt.plot(x, y, v['legend'], label=k)
                else:
                    plt.plot(range(len(value[k])), value[k], v['legend'], label=k)

        if x_label:
            plt.xticks(range(len(value[x_label])), value[x_label], horizontalalignment='right', rotation=30, fontsize='small')
        #     fmt = FormatTime(value[x_label])
        #     ax = plt.gca()
        #     ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt.format_date))
        plt.legend()
