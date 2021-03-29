import pandas as pd
import altair as alt
import tqdm

df = pd.read_csv('../../processed_data/ampc_ap.csv')
line = alt.Chart(df).mark_line().encode(
    x = alt.X('Training size', title='Training set size'),
    y = alt.Y('Average Precision', aggregate='mean')
)
pts =  alt.Chart(df).mark_point().encode(
    x = alt.X('Training size', title='Training set size'),
    y = alt.Y('Average Precision', aggregate='mean')
)
eb = alt.Chart(df).mark_errorbar(extent='ci').encode(
    x = alt.X('Training size', title='Training set size'),
    y = alt.Y('Average Precision')
)

panel_a = (line.properties(height=200)+eb+pts)



##Now plot the estimate of 0.3th percentile cut-off

pdf = pd.read_csv('../../processed_data/ampc_cutoff.csv')
ch = alt.Chart(pdf)
panel_b = ch.mark_line(opacity=0.1).encode(
    x = alt.X('x', title='Training set size'),
    y = alt.Y('y', title='0.3% estimate', scale=alt.Scale(zero=False)),
    detail = 'i'
    #color=alt.Color('i')
)

(panel_a & panel_b.properties(height=200)).save('../../figures/ampc_ap.html')
