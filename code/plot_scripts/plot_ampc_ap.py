import pandas as pd
import altair as alt

df = pd.read_csv('../../processed_data/ampc_ap.csv')
line = alt.Chart(df).mark_line().encode(
    x = alt.X('Training size'),
    y = alt.Y('Average Precision', aggregate='mean')
)
pts =  alt.Chart(df).mark_point().encode(
    x = alt.X('Training size'),
    y = alt.Y('Average Precision', aggregate='mean')
)
eb = alt.Chart(df).mark_errorbar(extent='ci').encode(
    x = alt.X('Training size'),
    y = alt.Y('Average Precision')
)

(line+eb+pts).save('../../figures/ampc_ap.html')
