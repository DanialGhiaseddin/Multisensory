import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psychopy.gui


def get_nearset_index(numbers_list, query):
    query_np = np.asarray([query] * len(numbers_list))
    numbers_np = np.asarray(numbers_list)
    diff = np.abs(query_np - numbers_np)
    return numbers_list[np.argmin(diff)]


def make_hist(ax, x, bins=None, binlabels=None, width=0.85, extra_x=1, extra_y=4,
              text_offset=0.3, title=r"Frequency diagram",
              xlabel="Values", ylabel="Frequency"):
    if bins is None:
        xmax = max(x) + extra_x
        bins = range(xmax + 1)
    if binlabels is None:
        if np.issubdtype(np.asarray(x).dtype, np.integer):
            binlabels = [str(bins[i]) for i in range(len(bins))]
        else:
            binlabels = [str(bins[i]) if bins[i + 1] - bins[i] == 1 else
                         '{}-{}'.format(*bins[i:i + 2])
                         for i in range(len(bins) - 1)]
        if bins[-1] == np.inf:
            binlabels[-1] = '{}+'.format(bins[-2])
    n, bins = np.histogram(x, bins=bins + [400])
    patches = ax.bar(range(len(n)), n, align='center', width=width)
    ymax = max(n) + extra_y

    ax.set_xticks(range(len(binlabels)))
    ax.set_xticklabels(binlabels)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, ymax)
    ax.grid(True, axis='y')
    # http://stackoverflow.com/a/28720127/190597 (peeol)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # http://stackoverflow.com/a/11417222/190597 (gcalmettes)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    autolabel(patches, text_offset)


def autolabel(rects, shift=0.3):
    """
    http://matplotlib.org/1.2.1/examples/pylab_examples/barchart_demo.html
    """
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        if height > 0:
            plt.text(rect.get_x() + rect.get_width() / 2., height + shift, '%d' % int(height),
                     ha='center', va='bottom')


def compute_compensation_offset(file_name):
    df = pd.read_csv(file_name)
    cmds = df['delay.command']
    meds = df['delay.measured']
    return np.mean(meds - cmds)


if __name__ == "__main__":
    gui = psychopy.gui.Dlg()
    gui.addField("Result File Path:")

    gui.show()

    assert gui.data[0] != ""

    dataframe = pd.read_csv(gui.data[0])

    commands = dataframe['delay.command']
    measured = dataframe['delay.measured']
    # measured = dataframe['delay.measured']

    print("Total offset:", np.mean(measured - commands))

    delays_dict = dict()
    delay_range = [-300, -200, -100, -50, -20, -10, 0, 10, 20, 50, 100, 200, 300]
    for index, row in dataframe.iterrows():
        delay_command = row['delay.command']
        delay_value = row['delay.measured']
        response = row['response.key']
        if response.__contains__('space'):
            response = 1
        else:
            response = 0
        # delay_value = round(delay_value / 10) * 10
        delay_value = get_nearset_index(delay_range, delay_value)
        temp = row['response.key']
        if delay_value in delays_dict:
            delays_dict[delay_value][0] += 1
            delays_dict[delay_value][1] += response  # row['response.key']
        else:
            delays_dict[delay_value] = [1, response]

    x_values = sorted(delays_dict.keys())
    y_values = []
    for x in x_values:
        # y_values.append(delays_dict[x][1] / delays_dict[x][0])
        y_values += ([x] * delays_dict[x][0])

    # plt.hist(y_values)
    # plt.plot(x_values, y_values)
    # plt.show()
    # exit()

    # x = [6,0,0,26,0,0,0,0,5,0,7,0,12,12,0,0,0,3,0,5,5,0,10,4,3,5,1,0,2,0,0,1,0,8,0,
    #      3,7,1,0,0,0,1,1,0,0,0,0,0,7,16,0,0,0,5,41]
    fig, ax = plt.subplots(figsize=(14, 5))
    # make_hist(ax, x)
    # make_hist(ax, [1,1,1,0,0,0], extra_y=1, text_offset=0.1)
    make_hist(ax, y_values, bins=x_values)
    plt.show()
