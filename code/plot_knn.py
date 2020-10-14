import altair as alt
import numpy as np
import pandas as pd

df = pd.DataFrame(columns=['Average Precision', 'Fingerprint Size', 'k'])
count = 0
sizes = [64<<i for i in range(11)]
for fpSize in sizes:
    try:
        results = np.load(f'../processed_data/knn_'+str(fpSize)+'.npy', 'r')
    except:
        continue
    
    for res, k in zip(results[::5], np.arange(1,12000)[::5]):
        df.loc[count]=[res,fpSize, k]
        count+=1



lines = alt.Chart(df).mark_point(size=3).encode(
    x=alt.X('k', ),
    y=alt.Y('Average Precision', ),
    color=alt.Color('Fingerprint Size:N',)# scale=alt.Scale(type='log',base=2, domain=(30,70000), zero=False)),
#scale=alt.Scale(type='log',base=2, domain=(low,high), zero=False)
)

hline = alt.Chart(df).mark_rule(size=1, strokeDash=[10, 10]).encode(
    y=alt.Y('a:Q'),
)

ch = (lines+hline).transform_calculate(a="0.013")
ch.save('../processed_data/knn.html')
