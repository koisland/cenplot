import polars as pl

from .bed9 import read_bed9


def read_bed_label(infile: str, *, chrom: str | None = None) -> pl.DataFrame:
    df_track = read_bed9(infile, chrom=chrom)

    # Order facets by descending length. This prevents larger annotations from blocking others.
    fct_name_order = (
        df_track.group_by(["name"])
        .agg(len=(pl.col("chrom_end") - pl.col("chrom_st")).sum())
        .sort(by="len", descending=True)
        .get_column("name")
    )
    return df_track.cast({"name": pl.Enum(fct_name_order)})
