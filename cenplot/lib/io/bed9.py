import polars as pl

from .adj_ctg_coords import adj_by_ctg_coords
from ..defaults import BED9_COL_MAP


def read_bed9(infile: str, *, chrom: str | None = None) -> pl.DataFrame:
    df = pl.read_csv(infile, separator="\t", has_header=False)
    df = df.rename({col: val for col, val in BED9_COL_MAP.items() if col in df.columns})
    df_adj = adj_by_ctg_coords(df, "chrom").sort(by="chrom_st")

    if chrom:
        df_adj = df_adj.filter(pl.col("chrom") == chrom)
    if "item_rgb" not in df.columns:
        df_adj = df_adj.with_columns(item_rgb=pl.lit("0,0,0"))
    if "name" not in df.columns:
        df_adj = df_adj.with_columns(name=pl.lit("-"))

    return df_adj
