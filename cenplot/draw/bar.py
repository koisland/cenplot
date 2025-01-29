import ast
from matplotlib.axes import Axes
from matplotlib.colors import rgb2hex


from .utils import draw_uniq_entry_legend, format_ax
from ..track.types import Track


def draw_bars(
    ax: Axes,
    track: Track,
    *,
    zorder: float,
    legend_ax: Axes | None = None,
) -> None:
    hide_x = track.options.hide_x
    color = track.options.color
    alpha = track.options.alpha
    legend = track.options.legend

    format_ax(
        ax,
        xticks=hide_x,
        xticklabel_fontsize=track.options.fontsize,
        yticklabel_fontsize=track.options.fontsize,
        spines=("right", "top"),
    )

    plot_options = {"zorder": zorder, "alpha": alpha}
    if color:
        plot_options["color"] = color
    elif "item_rgb" in track.data.columns:
        # Convert colors from rgb str -> rgb tuple -> hex
        color = [
            rgb2hex([c / 255 for c in ast.literal_eval(rgb)])
            for rgb in track.data.get_column("item_rgb")
        ]
        plot_options["color"] = color
    else:
        plot_options["color"] = track.options.DEF_COLOR

    # Add bar
    ax.bar(
        track.data["chrom_st"],
        track.data["name"],
        track.data["chrom_end"] - track.data["chrom_st"],
        **plot_options,
    )
    # Trim plot to margins
    ax.margins(x=0, y=0)

    # Limit spine range.
    ax.spines["bottom"].set_bounds(0, track.data["chrom_end"].max())

    if legend_ax and legend:
        draw_uniq_entry_legend(legend_ax, track, ref_ax=ax, loc="center left", ncols=3)
