import logging
from conversant.data.vizualizations.barplots import percentile_plot

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)


def posts_per_conversation(df) -> bool:
    """
        :parameter:  df - pandas dataframe containing conversations 

        prints a percentile plot of number of posts per conversation
    """
    percentiles = list(df.groupby('tree_id').node_id.count().
                       sort_values(ascending=False).describe())[4:7]
    node_stats = {'25 percentile': percentiles[0], '50 percentile': percentiles[1],
                                                   '75 percentile': percentiles[2]}
    percentile_plot(node_stats, '#posts per tree', 'Posts per conversation')

    return True
