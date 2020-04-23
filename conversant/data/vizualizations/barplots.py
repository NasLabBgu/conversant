import matplotlib.pyplot as plt

import logging
logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def percentile_plot(percentiles: dict, ylabel: str, title: str, color=None):
    """ Prints a percentile plot of some data
    
    Arguments:
        percentiles {dict} -- dictionary of the form {'string' : float}
        ylabel {str} -- text to be placed in the y axis
        title {str} -- text to be placed as title
    
    Keyword Arguments:
        color {list} -- list of strings indicating which bar plot colors to choose (default: {None})
    """

    fig, ax = plt.subplots(figsize=(10, 5))

    if color is None:
        color = ['m', 'blueviolet', 'indigo', 'darkblue']

    rects1 = ax.bar(range(len(percentiles)), list(percentiles.values()),
                    align='center', color=color)
    plt.xticks(range(len(percentiles)), list(percentiles.keys()))

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects1)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    fig.tight_layout()

    plt.show()