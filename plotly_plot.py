from backtrader_plotly.scheme import PlotScheme
from backtrader_plotly.plotter import BacktraderPlotly
import plotly.io

def plot_using_plotly():
    scheme = PlotScheme(decimal_places=2, max_legend_text_width=12)
    figs = cerebro.plot(BacktraderPlotly(show=False, scheme=scheme))

    # directly manipulate object using methods provided by `plotly`
    for i, each_run in enumerate(figs):
        for j, each_strategy_fig in enumerate(each_run):
            # open plot in browser
            each_strategy_fig.show()

            # save the html of the plot to a variable
            html = plotly.io.to_html(each_strategy_fig, full_html=False)

            # write html to disk
            plotly.io.write_html(each_strategy_fig, f'{i}_{j}.html', full_html=True)