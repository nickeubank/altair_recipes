#########
# Imports
#########

import altair as alt
import altair_saver

alt.data_transformers.enable("data_server")


def scatter_with_reg(df, xvar, yvar, input_color="black", order=1, type="reg"):

    # Groups
    grouped_means = df.groupby(xvar, as_index=False)[[yvar]].mean()

    # Grouped scatter
    chart_grouped = (
        alt.Chart(grouped_means)
        .mark_circle(color=input_color, opacity=0.5)
        .encode(
            x=alt.X(xvar, scale=alt.Scale(zero=False)),
            y=alt.Y(yvar, scale=alt.Scale(zero=False)),
        )
    )

    # Fit model
    if type == "reg":
        fit = (
            alt.Chart(df)
            .encode(
                x=alt.X(xvar, scale=alt.Scale(zero=False)),
                y=alt.Y(yvar, scale=alt.Scale(zero=False)),
            )
            .transform_regression(
                xvar,
                yvar,
                method="poly",
                order=order,
            )
            .mark_line(color=input_color)
        )
    elif type == "loess":
        fit = (
            alt.Chart(df)
            .encode(
                x=alt.X(xvar, scale=alt.Scale(zero=False)),
                y=alt.Y(yvar, scale=alt.Scale(zero=True)),
            )
            .transform_loess(on=xvar, loess=yvar, bandwidth=1)
            .mark_line(color=input_color)
        )
    return chart_grouped + fit


####
# Make all four components
####


def diff_in_diff_plot(dfs, xvar, yvar, order=1, type="reg"):
    charts = dict()
    colors = {0: "black", 1: "red"}
    for t in [0, 1]:
        for part in [0, 1]:
            charts[(t, part)] = scatter_with_reg(
                dfs[(t, part)],
                xvar,
                yvar,
                input_color=colors[t],
                order=order,
                type=type,
            )
    return alt.layer(*charts.values())


# # Example Data Split
# dfs = dict()
# for t in [0, 1]:
#     dfs[(t, 0)] = df[(df.treatment_ever_treated == t) & (df.year < 2017)]
#     dfs[(t, 1)] = df[(df.treatment_ever_treated == t) & (df.year >= 2017)]

# # Test part
# scatter_with_reg(
#     dfs[(0, 0)], "years_w_decimals", "part2_arrest_rate_1000_total", order=2
# )

# # Test all
# diff_in_diff_plot(dfs, "years_w_decimals", "part2_arrest_rate_1000_total", order=3)
