import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_learning_curves(x:str, y:str, hue:str, data:pd.DataFrame, title:str, xticks:list = [], fix_y_axis=False):
    """ Plotting learning curves
    
    Arguments:
        x {str} -- the x dimension of the plot
        y {str} -- the y dimension of the plot
        hue {str} -- split by hue(same as seaborn)
        data {pd.DataFrame} -- pandas dataframe containing plot data 
        xticks {list} -- values to present over the x axis <optional>
        title {str} -- title to display
    
    Keyword Arguments:
        fix_y_axis {bool} -- option to fix the y axis between 0,1 (default: {False})
    """
    _, ax = plt.subplots(figsize= (12, 4))
    if fix_y_axis:
        ax.set_ylim([0,1])
    ax.set_xticks(xticks)
    plt.xticks(rotation=90)
    sns.pointplot(x=x, y=y, hue=hue, data=data, ax=ax)
    plt.title(title)
    plt.show()