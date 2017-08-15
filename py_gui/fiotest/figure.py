import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_all(all_data, data_to_plot, x_label=None):
    for key, value in all_data.items():
        if value:
            plot_time_y(value, data_to_plot[key], x_label)
    plt.savefig('test.png', dpi=160)
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
