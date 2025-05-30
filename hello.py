import pandas as pd
import numpy as np
import plotly.express as px
import preswald
from preswald import connect, get_df
# connect()
# df = get_df("finance")
df = pd.read_csv("data/finance.csv")

df = df[df["Totals.Revenue"].notna() & df["Totals.Expenditure"].notna()]
np.random.seed(42)
df["lat"] = np.random.uniform(25, 49, size=len(df))
df["lon"] = np.random.uniform(-125, -67, size=len(df))

fig1 = px.scatter(
    df,
    x="Totals.Revenue",
    y="Totals.Expenditure",
    color="State",
    hover_name="State",
    title="Revenue vs. Expenditure by State"
)

fig2 = px.density_mapbox(
    df,
    lat="lat",
    lon="lon",
    radius=10,
    zoom=3,
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    title="Revenue Density Map"
)

revenue_sources = [
    "Totals.Tax",
    "Details.Miscellaneous general revenue",
    "Details.Education.Education Total"
]
df["revenue_richness"] = df[revenue_sources].gt(0).sum(axis=1)
richness = df.groupby("State")["revenue_richness"].mean().reset_index(name="richness")

fig3 = px.bar(
    richness.sort_values("richness", ascending=False),
    x="State",
    y="richness",
    title="Revenue Source Richness"
)

df_treemap = df[["State"] + revenue_sources].melt(
    id_vars="State", var_name="Source", value_name="Amount"
)
fig4 = px.treemap(
    df_treemap,
    path=["State", "Source"],
    values="Amount",
    color="Amount",
    title="Revenue Composition Treemap"
)

fig5 = None
if "Year" in df.columns:
    trend_data = df.groupby("Year")["Totals.Expenditure"].sum().reset_index(name="Total_Expenditure")
    fig5 = px.line(
        trend_data,
        x="Year",
        y="Total_Expenditure",
        title="Total Expenditure Over Time"
    )

preswald.text("# U.S. State Finance Explorer")
preswald.text("## Revenue vs. Expenditure")
preswald.plotly(fig1)

preswald.text("## Revenue Density Map")
preswald.plotly(fig2)

preswald.text("## Revenue Source Richness")
preswald.plotly(fig3)

preswald.text("## Revenue Composition Treemap")
preswald.plotly(fig4)

if fig5:
    preswald.text("## Expenditure Over Time")
    preswald.plotly(fig5)
