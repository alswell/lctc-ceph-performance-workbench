from Tkinter import *
import settings
import fiotest
from utils import get_data, parse_data
from figure import plot_all


PAGE_SIZE = 10
PAGE_INFO = "page: %s; total: %s"


class App(Frame):
    def __init__(self, master):
        self.result_widget = {
            'check': [],
            'checkbox': [],
            'id': [],
        }
        self.result_column = settings.RESULT_COLUMN
        master.title("fio test")
        self.frame = Frame(master)
        self.frame.grid()
        self.row = 0

        self.result_check = []
        self.result = get_data('fiotest')["data"]
        for i in range(len(self.result)):
            self.result_check.append(False)

        self.cur_page = 0
        self.total_page = len(self.result) / PAGE_SIZE
        self._init_page(self.cur_page)

        Button(self.frame, width=10, text='PLOT', command=self._plot).grid(row=self.row, column=7)
        Label(self.frame, text='      ').grid(row=self.row, column=8, sticky=E)
        Label(self.frame, text='      ').grid(row=self.row, column=9, sticky=E)
        Label(self.frame, text='query:').grid(row=self.row, column=10, sticky=E)
        self.txt = Text(self.frame, height=15, wrap=WORD)
        self.txt.grid(row=self.row, column=11, rowspan=10, columnspan=20, sticky=W)

        self.y_label = IntVar()
        Radiobutton(self.frame, text="Y-metric", variable=self.y_label, value=1).grid(row=self.row, column=1)
        Radiobutton(self.frame, text="Y-job_id", variable=self.y_label, value=2).grid(row=self.row, column=5)
        Radiobutton(self.frame, text="Y-result", variable=self.y_label, value=3).grid(row=self.row, column=6)
        self.row += 1

        self.to_plot = []
        self._init_y_metric()
        self._init_y_job_id()
        self._init_y_result()

        master.mainloop()

    def _init_page(self, page_num):
        Label(self.frame, text='X-metric').grid(row=self.row, column=0, sticky=W)
        Label(self.frame, text='X-jobid|result').grid(row=self.row, column=1, sticky=E)
        first_column = 2
        column = first_column
        for rst_col in self.result_column:
            columnspan = rst_col['width'] / 10
            Label(self.frame, text=rst_col['name']).grid(row=self.row, column=column, columnspan=columnspan, sticky=W)
            self.result_widget[rst_col['name']] = []
            column += columnspan

        self.radio = IntVar()
        for i in range(PAGE_SIZE):
            n = PAGE_SIZE * page_num + i
            self.row += 1

            Radiobutton(self.frame, variable=self.radio, value=i+1).grid(row=self.row, column=0, sticky=E)
            b1 = BooleanVar()
            v1 = StringVar()
            checkbox = Checkbutton(self.frame, textvariable=v1, variable=b1)
            try:
                v1.set("%03d" % self.result[n].get('id', -1))
            except IndexError:
                v1.set('000')
            checkbox.grid(row=self.row, column=1, sticky=E)
            self.result_widget['checkbox'].append(checkbox)
            self.result_widget['id'].append(v1)
            self.result_widget['check'].append(b1)

            column = first_column
            for rst_col in self.result_column:
                width = rst_col['width']
                columnspan = width / 10
                v1 = StringVar()
                Entry(self.frame, width=width, textvariable=v1, stat="readonly").grid(row=self.row, column=column, columnspan=columnspan)
                try:
                    v1.set(self.result[n][rst_col['name']])
                except IndexError:
                    v1.set('')
                self.result_widget[rst_col['name']].append(v1)
                column += columnspan

        self.row += 1
        Button(self.frame, text='<<', command=self._prior_page).grid(row=self.row, column=1, sticky=E)
        self.page_info = StringVar()
        Entry(self.frame, textvariable=self.page_info, stat="readonly").grid(row=self.row, column=2, columnspan=3)
        self._update_page_info()
        Button(self.frame, text='>>', command=self._next_page).grid(row=self.row, column=5, sticky=W)

        # Button(self.frame, text='QUERY', command=self._query).grid(row=self.row, column=10, sticky=E)
        # self.result_filter = {}
        # for i in range(2, 9):
        #     v1 = StringVar()
        #     Entry(self.frame, width=self.result_column[i]['width'], textvariable=v1).grid(row=self.row, column=10+i)
        #     self.result_filter[self.result_column[i]['name']] = v1

        self.row += 1

    def _init_y_metric(self):
        column = 0
        y_metric = fiotest.get_y_metric()
        self.to_plot.append(y_metric)
        key_map = {
            'sarcpu': 'CPU',
            'sarmem': 'Memory',
            'sarnic': 'NIC',
        }
        for key, value in y_metric.items():
            column += 1
            row = self.row
            Label(self.frame, text=key_map.get(key, key)).grid(row=row, column=column, sticky=W)
            row += 1
            for k, v in value.items():
                need_plot = BooleanVar()
                y_metric[key][k] = {'legend': v, 'need_plot': need_plot}
                Checkbutton(self.frame, text=k, variable=need_plot).grid(row=row, column=column, sticky=W)
                row += 1

    def _init_y_job_id(self):
        y_job_id = {
            # "iops": {'legend': "co-"},
            # "lat": {'legend': "mo-"},
            # "bw": {'legend': "yo-"},
        }
        self.to_plot.append({'result': y_job_id})
        # row = self.row + 1
        # for key, value in y_job_id.items():
        #     need_plot = BooleanVar()
        #     y_job_id[key]['need_plot'] = need_plot
        #     Checkbutton(self.frame, text=key, variable=need_plot).grid(row=row, column=5, sticky=W)
        #     row += 1

    def _init_y_result(self):
        y_result = {
            "iops": {'legend': "co-"},
            "lat": {'legend': "mo-"},
            "bw": {'legend': "yo-"},
        }
        self.to_plot.append({'result': y_result})
        row = self.row + 1
        for key, value in y_result.items():
            need_plot = BooleanVar()
            y_result[key]['need_plot'] = need_plot
            Checkbutton(self.frame, text=key, variable=need_plot).grid(row=row, column=6, sticky=W)
            row += 1

    def _show_page(self, page_num):
        for i in range(PAGE_SIZE):
            n = PAGE_SIZE * page_num + i
            try:
                if self.result_check[n]:
                    self.result_widget['checkbox'][i].select()
                else:
                    self.result_widget['checkbox'][i].deselect()

                self.result_widget['id'][i].set("%03d" % self.result[n].get('id', -1))
                for column in self.result_column:
                    self.result_widget[column['name']][i].set(self.result[n][column['name']])
            except IndexError:
                self.result_widget['id'][i].set("000")
                self.result_widget['checkbox'][i].deselect()
                for column in self.result_column:
                    self.result_widget[column['name']][i].set("")

    def _save_check(self):
        for i in range(PAGE_SIZE):
            try:
                n = PAGE_SIZE * self.cur_page + i
                self.result_check[n] = self.result_widget['check'][i].get() == 1
            except IndexError:
                pass

    def _set_status_txt(self, message):
        self.txt.delete(0.0, END)
        self.txt.insert(0.0, message)

    def _update_page_info(self):
        self.page_info.set(PAGE_INFO % (self.cur_page + 1, self.total_page + 1))

    def _next_page(self):
        if self.cur_page == self.total_page:
            return
        self._save_check()
        self.cur_page += 1
        self._show_page(self.cur_page)
        self._update_page_info()

    def _prior_page(self):
        if self.cur_page == 0:
            return
        self._save_check()
        self.cur_page -= 1
        self._show_page(self.cur_page)
        self._update_page_info()

    # def _on_check(self):
    #     cur_check = -1
    #     for i in range(PAGE_SIZE):
    #         try:
    #             n = PAGE_SIZE * self.cur_page + i
    #             if self.result_check[n] != (self.result_widget['check'][i].get() == 1):
    #                 self.result_widget['checkbox'][i].select()
    #                 cur_check = n
    #             else:
    #                 self.result_widget['checkbox'][i].deselect()
    #         except IndexError:
    #             pass
    #
    #     for i in range(len(self.result_check)):
    #         self.result_check[i] = cur_check == i

    def _query(self):
        self._save_check()
        print self.result_check
        query_data = fiotest.query_result(self.result_filter)
        self._set_status_txt("_query: %s" % query_data)

    def _plot(self):
        self._save_check()

        case_id = PAGE_SIZE * self.cur_page + self.radio.get()
        self._set_status_txt("case id: %s" % case_id)

        if self.y_label.get() == 1:
            all_data = {}
            for key, value in self.to_plot[0].items():
                need_plot = False
                for k, v in value.items():
                    if v['need_plot'].get() == 1:
                        need_plot = True
                        break
                if need_plot:
                    all_data[key] = {}
            for key, _ in all_data.items():
                for node, node_value in get_data(key, case_id).items():
                    all_data[key][node] = parse_data(node_value)
            # plot_all(all_data, self.to_plot[0], 'time')
            plot_all(all_data, self.to_plot[0])

        elif self.y_label.get() == 2:
            result = [self.result[i] for i in range(len(self.result)) if self.result_check[i]]
            if not result:
                return
            legends = settings.LEGEND
            legend_index = 0
            keys = ['iodepth', 'numberjob', 'imagenum', 'clientnum']
            all_data = {'result': {}}
            for key, value in self.to_plot[2]['result'].items():
                if value['need_plot'].get() == 1:
                    all_data['result'][key] = {}
            x_label = {}
            for item in result:
                name = item['blocksize']
                for key in keys:
                    name += '_%s%s' % (key, item[key])
                name += '_' + item['readwrite']

                x_label[name] = True
                if self.to_plot[1]['result'].get(item['jobid']) is None:
                    b = BooleanVar()
                    b.set(1)
                    self.to_plot[1]['result'][item['jobid']] = {'legend': legends[legend_index], 'need_plot': b}
                    legend_index += 1

                for key, _ in all_data['result'].items():
                    try:
                        all_data['result'][key][item['jobid']].update({name: item[key]})
                    except KeyError:
                        all_data['result'][key][item['jobid']] = {}
                        all_data['result'][key][item['jobid']].update({name: item[key]})
            names = [k for k, v in x_label.items()]
            for key, _ in all_data['result'].items():
                all_data['result'][key]['name'] = names
            plot_all(all_data, self.to_plot[1], 'name')

        elif self.y_label.get() == 3:
            result = [self.result[i] for i in range(len(self.result)) if self.result_check[i]]
            if result:
                all_data = {'result': {}}
                all_data['result']['fiotest'] = parse_data(result)
                plot_all(all_data, self.to_plot[2], 'case_name')


app = App(Tk())
