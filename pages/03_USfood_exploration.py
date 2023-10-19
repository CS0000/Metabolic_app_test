from helper import *
import plotly.express as px
from plotly.subplots import make_subplots

sheet_id = '1TK83ei6J6bmQRyo-2nd-N1UPbUbXtgMldmtrwS2rcSA'
df_id = 'df_RA_fianl'
lookup_id = 'HICL%20Lookup'

url_df = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={df_id}"
url_match = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={lookup_id}"
df_RA_final = pd.read_csv(url_df)
match_df = pd.read_csv(url_match)

df_RA_final['Product Description Short'] = df_RA_final['Product Description'].apply(lambda x: x.split(' ')[0])
df_RA_final['Main Ingredient group'] = df_RA_final['PIM Group'].apply(lambda x: x.split(' ')[0])
df_RA_final_HICL = df_RA_final.merge(match_df,on=['Product Description Short','Main Ingredient group'],how='left')
df_RA_final_HICL_splitCountry = df_RA_final_HICL.assign(**{'Country of Origin': df_RA_final_HICL['Country of Origin'].str.split(',')}).explode('Country of Origin').reset_index(drop=True)

df = df_RA_final_HICL_splitCountry.loc[:,['HICL','Merch Category','PIM Group','Net Weight Received','Country of Origin']]
df = df.loc[(df['HICL'].notnull())&(df['HICL']!=''),:]
print(df['HICL'].unique().tolist())
print(df.shape)
print(df)
# select_list = ['Sugarcane','Rice']
relative = st.sidebar.checkbox('Proportion')

select_list = st.sidebar.multiselect(
    'select HICL',
    df['HICL'].unique().tolist(),
    ['Sugarcane','Rice'])

# fig = make_subplots(rows=2, cols=1)

df_filter = df.loc[df['HICL'].isin(select_list),:]

if relative:
    pass


fig_pim = px.bar(df_filter.groupby('PIM Group').sum().reset_index().sort_values('Net Weight Received',ascending=False).iloc[0:20,:],
                 x='PIM Group', y='Net Weight Received',
                 title=f"Net Weight Received - PIM Group")
fig_merch = px.bar(df_filter.groupby('Merch Category').sum().reset_index().sort_values('Net Weight Received',ascending=False).iloc[0:20,:],
                   x='Merch Category', y='Net Weight Received',
                   title=f"Net Weight Received - Merch Category")

for fig in [fig_pim,fig_merch]:
    fig.update_xaxes(tickangle=75)
    fig.update_traces(marker_color='#b52451')
    st.plotly_chart(fig, use_container_width=True)