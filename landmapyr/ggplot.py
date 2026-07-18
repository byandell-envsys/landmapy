from plotnine import ggplot, aes
from plotnine import geom_jitter, geom_abline, stat_smooth, geom_path
from plotnine import scale_x_log10, scale_y_log10

def ggplot_xy(df, x, y, z=None, log=None, identity=False, method="lm"):
    """
    Plot x-y data with optional log scaling and identity line.

    Args:
        df (df): Dataframe with x and y columns.
        x (str): name of x column.
        y (str): name of y column.
        z (str, optional): name of z column. Defaults to None.
        log (str, optional): Log tranform x and/or y. Defaults to None.
        identity (bool, optional): Add identity line. Defaults to False.
        method (str, optional): Method for smoothing. Defaults to "lm".

    Returns:
        p: ggplot object
    """
    p = (
        ggplot(df)
            + aes(x, y)
            + geom_jitter(width=0.25, height=0.1, size=0.5, alpha=0.25, color="grey")
    )
    if not z is None:
        p += aes(color=z)
    if not method is None:
        p += stat_smooth(se=False, method=method, span=0.25, color="blue")
    else:
        p += geom_path()
    if not log is None:
        p += scale_x_log10() if "x" in log else None
        p += scale_y_log10() if "y" in log else None
    if identity:
        p += geom_abline(intercept=0, slope=1, linetype="dashed", color="red")

    return p

# ggplot_xy(df)
