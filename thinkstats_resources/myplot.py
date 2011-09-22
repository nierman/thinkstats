"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

import math
import matplotlib
import matplotlib.pyplot as pyplot

# customize some matplotlib attributes
#matplotlib.rc('figure', figsize=(4, 3))

matplotlib.rc('font', size=14.0)
#matplotlib.rc('axes', labelsize=22.0, titlesize=22.0)
#matplotlib.rc('legend', fontsize=20.0)

#matplotlib.rc('xtick.major', size=6.0)
#matplotlib.rc('xtick.minor', size=3.0)

#matplotlib.rc('ytick.major', size=6.0)
#matplotlib.rc('ytick.minor', size=3.0)


class InfiniteList(list):
    def __init__(self, val):
        self.val = val

    def __getitem__(self, index):
        return self.val


def Underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    If d is None, create a new dictionary.
    """
    if d is None:
        d = {}

    for key, val in options.iteritems():
        d.setdefault(key, val)

    return d


def Plot(xs, ys, clf=True, root=None, line_options=None, **options):
    """Plots a Pmf or Hist as a line.

    Args:
      pmf: Hist or Pmf object
      clf: boolean, whether to clear the figure      
      root: string filename root
      line_options: dictionary of options passed to pylot.plot
      options: dictionary of options
    """
    if clf:
        pyplot.clf()

    line_options = Underride(line_options, linewidth=2)

    pyplot.plot(xs, ys, **line_options)
    Save(root=root, **options)


def Pmf(pmf, clf=True, root=None, line_options=None, **options):
    """Plots a Pmf or Hist as a line.

    Args:
      pmf: Hist or Pmf object
      clf: boolean, whether to clear the figure      
      root: string filename root
      line_options: dictionary of options passed to pylot.plot
      options: dictionary of options
    """
    xs, ps = pmf.Render()
    line_options = Underride(line_options, label=pmf.name)

    Plot(xs, ps, clf, root, line_options, **options)


def Pmfs(pmfs,
         clf=True,
         root=None, 
         plot_options=InfiniteList(dict(linewidth=2)), 
         **options):
    """Plots a sequence of PMFs.
    
    Args:
      pmfs: sequence of PMF objects
      clf: boolean, whether to clear the figure
      root: string root of the filename to write
      plot_options: sequence of option dictionaries
      options: dictionary of keyword options passed along to Save
    """
    if clf:
        pyplot.clf()

    styles = options.get('styles', None)
    if styles is None:
        styles = InfiniteList('-')

    for i, pmf in enumerate(pmfs):
        
        xs, ps = pmf.Render()

        line = pyplot.plot(xs, ps,
                           styles[i],
                           label=pmf.name,
                           **plot_options[i]
                           )

    Save(root, **options)


def Hist(hist, clf=True, root=None, bar_options=None, **options):
    """Plots a Pmf or Hist with a bar plot.

    Args:
      hist: Hist or Pmf object
      clf: boolean, whether to clear the figure
      root: string filename root
      bar_options: dictionary of options passed to pylot.bar
      options: dictionary of options
    """
    if clf:
        pyplot.clf()

    # find the minimum distance between adjacent values
    xs, fs = hist.Render()
    width = min(Diff(xs))

    bar_options = Underride(bar_options, 
                            label=hist.name,
                            align='center',
                            edgecolor='blue',
                            width=width)

    pyplot.bar(xs, fs, **bar_options)
    Save(root=root, **options)


def Hists(hists, 
          clf=True,
          root=None,
          bar_options=InfiniteList(dict()),
          **options):
    """Plots two histograms as interleaved bar plots.

    Args:
      hists: list of two Hist or Pmf objects
      clf: boolean, whether to clear the figure
      root: string filename root
      bar_options: sequence of option dictionaries
      options: dictionary of options
    """
    if clf:
        pyplot.clf()

    width = 0.4
    shifts = [-width, 0.0]

    for i, hist in enumerate(hists):
        xs, fs = hist.Render()
        xs = Shift(xs, shifts[i])
        pyplot.bar(xs, fs, label=hist.name, width=width, **bar_options[i])

    Save(root=root, **options)


def Shift(xs, shift):
    """Adds a constant to a sequence of values.

    Args:
      xs: sequence of values

      shift: value to add

    Returns:
      sequence of numbers
    """
    return [x+shift for x in xs]


def Diff(t):
    """Compute the differences between adjacent elements in a sequence.

    Args:
        t: sequence of number

    Returns:
        sequence of differences (length one less than t)
    """
    diffs = [t[i+1] - t[i] for i in range(len(t)-1)]
    return diffs


def Cdf(cdf, clf=True, root=None, plot_options=dict(linewidth=2), **options):
    """Plots a CDF as a line.

    Args:
      cdf: Cdf object
      clf: boolean, whether to clear the figure
      root: string filename root
      bar_options: dictionary of options passed to pylot.plot
      options: dictionary of options
    """
    Cdfs([cdf], clf=clf, root=root, plot_options=[plot_options], **options)


def Cdfs(cdfs,
         clf=True,
         root=None, 
         plot_options=InfiniteList(dict(linewidth=2)), 
         complement=False,
         transform=None,
         **options):
    """Plots a sequence of CDFs.
    
    Args:
      cdfs: sequence of CDF objects
      clf: boolean, whether to clear the figure
      root: string root of the filename to write
      plot_options: sequence of option dictionaries
      complement: boolean, whether to plot the complementary CDF
      options: dictionary of keyword options passed along to Save
    """
    if clf:
        pyplot.clf()

    styles = options.get('styles', None)
    if styles is None:
        styles = InfiniteList('-')

    for i, cdf in enumerate(cdfs):
        xs, ps = cdf.Render()

        if transform == 'exponential':
            complement = True
            options['yscale'] = 'log'

        if transform == 'pareto':
            complement = True
            options['yscale'] = 'log'
            options['xscale'] = 'log'

        if complement:
            ps = [1.0-p for p in ps]

        if transform == 'weibull':
            xs.pop()
            ps.pop()
            ps = [-math.log(1.0-p) for p in ps]
            options['xscale'] = 'log'
            options['yscale'] = 'log'

        if transform == 'gumbel':
            xs.pop(0)
            ps.pop(0)
            ps = [-math.log(p) for p in ps]
            options['yscale'] = 'log'

        line = pyplot.plot(xs, ps,
                           styles[i],
                           label=cdf.name,
                           **plot_options[i]
                           )

    Save(root, **options)


def Save(root=None, formats=None, **options):
    """Generate plots in the given formats.

    Pulls options out of the option dictionary and passes them to
    title, xlabel, ylabel, xscale, yscale, axis and legend.

    Args:
      root: string filename root
      formats: list of string formats
      options: dictionary of options
    """
    title = options.get('title', '')
    pyplot.title(title)

    xlabel = options.get('xlabel', '')
    pyplot.xlabel(xlabel)

    ylabel = options.get('ylabel', '')
    pyplot.ylabel(ylabel)

    if 'xscale' in options:
        pyplot.xscale(options['xscale'])

    if 'yscale' in options:
        pyplot.yscale(options['yscale'])

    if 'axis' in options:
        pyplot.axis(options['axis'])

    loc = options.get('loc', 0)
    legend = options.get('legend', True)
    if legend:
        pyplot.legend(loc=loc)

    if formats is None:
        formats = ['eps', 'png', 'pdf']

    if root:
        for format in formats:
            SaveFormat(root, format)

    show = options.get('show', False)
    if show:
        pyplot.show()


def SaveFormat(root, format='eps'):
    """Writes the current figure to a file in the given format.

    Args:
      root: string filename root

      format: string format
    """
    filename = '%s.%s' % (root, format)
    print 'Writing', filename
    pyplot.savefig(filename, format=format, dpi=300)


