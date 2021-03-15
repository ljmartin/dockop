
import pandas as pd
import altair as alt
import numpy as np



df1 = pd.read_csv('../../processed_data/D4_single_0.3.csv')
df1['Dataset'] = 'D4'

df2 = pd.read_csv('../../processed_data/AmpC_single_0.3.csv')
df2['Dataset'] = 'AmpC'


df = pd.concat([df1, df2])

df['gain'] = df['N hits wanted']/0.003 / df['N hits explored']
df['Days'] = df['N hits explored'] / 60 / 60 /24


cols = list(df.columns)
print(cols)
cols[2]='Training set size'

cols[-1] = 'Computation days (single cpu)'
df.columns = cols





##Plot single iteration, enrichment:
line = alt.Chart(df).mark_line(color='black',size=2,opacity=0.5).encode(
  x=alt.X('Training set size:Q', scale=alt.Scale(type='log')),
  y=alt.Y('gain',aggregate='mean',title='Enrichment'),
    color=alt.Color('N hits wanted:N')
)
pts = alt.Chart(df).mark_point(filled=False,size=40).encode(
  x=alt.X('Training set size:Q'),
  y=alt.Y('gain',aggregate='mean',title='Enrichment'),
    color=alt.Color('N hits wanted:N'),
    tooltip=alt.Tooltip('N hits wanted', aggregate='mean', title='Enrichment')
)

error_bars = alt.Chart(df).mark_errorbar(extent='ci').encode(
  x=alt.X('Training set size:Q',),
  y=alt.Y('gain', title='Enrichment'),
    color=alt.Color('N hits wanted:N')
)


ch = (line+pts+error_bars).properties(width=300, height=250).facet('Dataset:N')
ch.resolve_scale(y='independent').save('../../figures/single_it_enrichment.html')
#ch.save('../../figures/single_it_enrichment.html')



##Plot single iteration, computation days:
line = alt.Chart(df).mark_line(color='black',size=2,opacity=0.5).encode(
  x=alt.X('Training set size:Q', scale=alt.Scale(type='log')),
  y=alt.Y('Computation days (single cpu)',aggregate='mean',),
    color=alt.Color('N hits wanted:N')
)

pts = alt.Chart(df).mark_point(filled=False,size=40).encode(
  x=alt.X('Training set size:Q'),
  y=alt.Y('Computation days (single cpu)',aggregate='mean',),
    color=alt.Color('N hits wanted:N'),
#    tooltip=alt.Tooltip('Computation days (single cpu)')
)

error_bars = alt.Chart(df).mark_errorbar(extent='ci').encode(
  x=alt.X('Training set size:Q',),
  y=alt.Y('Computation days (single cpu)'),
    color=alt.Color('N hits wanted:N')
)

ch = line+pts+error_bars
ch = ch.properties(width=300, height=250).facet('Dataset:N',)


ch.resolve_scale(y='independent').save('../../figures/single_it_computationdays.html')
#ch.save('../../figures/single_it_computationdays.html')

#####
##Active learning approach:
#####
df1 = pd.read_csv('../../processed_data/ampc_reconstruction_0.3_1_.csv')
df1['Algorithm'] = 'AmpC:LogReg (ours)'
df2 = pd.read_csv('../../processed_data/D4_reconstruction_0.3_1_.csv')
df2['Algorithm'] = 'D4:LogReg (ours)'

df = pd.concat([df1, df2])

prev_results = [['AmpC:RF (Graff)', 400_000, 71.4, 2.1], ['AmpC:NN (Graff)', 400_000, 74.7, 1.4],
                ['AmpC:MPN (Graff)',400_000, 87.9, 2.3],
    ['AmpC:RF (Graff)', 200_000, 45.5, 1.8],
['AmpC:NN (Graff)', 200_000, 52.8, 0.5],
['AmpC:MPN (Graff)', 200_000, 67.1, 2.1],
['AmpC:RF (Graff)', 100_000, 24.0, 2.2],
['AmpC:NN (Graff)', 100_000 , 33.3,0.3],
['AmpC:MPN (Graff)', 100_000, 52.0, 0.5]]

coley = pd.DataFrame(columns=['Algorithm', 'Training size', 'N ligands explored', '% top-k found'])
count = 0 
for res in prev_results:
    
    desired_std_dev = res[3]
    samples = np.array([-1,0,1]).astype(float)
    samples *= (desired_std_dev/np.std(samples))
    for s in samples:
        coley.loc[count]= [res[0], res[1], res[1]*6, (s+res[2])/100]
        count+=1



concat = pd.concat([df, coley])
concat['% top-k found']*=100
concat.columns = ['nan', 'Algorithm', 'Training set size', 'N ligands explored', '% top-k found']
concat['Training set size'] = concat['Training set size'].apply(lambda num: f"{num:,d}",)
concat['Computation days (single CPU)'] = concat['N ligands explored'] / 60 / 60 /24



error_bars = alt.Chart(concat).mark_errorbar(extent='ci').encode(
  x=alt.X('N ligands explored:Q',title='Number of ligands sampled'),
  y=alt.Y('% top-k found:Q', title='% top 50,000 found'),
    color=alt.Color('Algorithm')
)

points = alt.Chart(concat).mark_point(filled=False, size=40, color='black').encode(
  x=alt.X('N ligands explored:Q'),
  y=alt.Y('% top-k found:Q',aggregate='mean',title='% top 50,000 found'),
    color=alt.Color('Algorithm'),
    tooltip=alt.Tooltip('% top-k found:Q',aggregate='mean',title='% top 50,000 found')
)

line = alt.Chart(concat).mark_line(color='black',size=2,opacity=0.5).encode(
  x=alt.X('N ligands explored:Q'),
  y=alt.Y('% top-k found:Q',aggregate='mean',title='% top 50,000 found'),
    color=alt.Color('Algorithm')
)

ch = (error_bars+points+line).properties(height=300,width=150).facet(
    column=alt.Column('Training set size:N',sort=alt.Sort([0.004, 0.002, 0.001])),
).resolve_scale(x='independent')
ch.save('../../figures/active_learning_percentage.html')



error_bars = alt.Chart(concat).mark_errorbar(extent='ci').encode(
  x=alt.X('Computation days (single CPU):Q',),
  y=alt.Y('% top-k found:Q', title='% top 50,000 found'),
    color=alt.Color('Algorithm')
)

points = alt.Chart(concat).mark_point(filled=False, size=40, color='black').encode(
  x=alt.X('Computation days (single CPU):Q'),
  y=alt.Y('% top-k found:Q',aggregate='mean',title='% top 50,000 found'),
    color=alt.Color('Algorithm'),
    tooltip=alt.Tooltip('Computation days (single CPU):Q')
)

line = alt.Chart(concat).mark_line(color='black',size=2,opacity=0.5).encode(
  x=alt.X('Computation days (single CPU):Q'),
  y=alt.Y('% top-k found:Q',aggregate='mean',title='% top 50,000 found'),
    color=alt.Color('Algorithm')
)

ch = (error_bars+points+line).properties(height=300,width=150).facet(
    column=alt.Column('Training set size:N',sort=alt.Sort([0.004, 0.002, 0.001])),
).resolve_scale(x='independent')
ch.save('../../figures/active_learning_computationdays.html')
