from helper import *
import plotly.express as px
# from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

metabolic_colors_20 = ['#a63246' ,'#e56e61' ,'#ea9243' ,'#ffc840' ,'#789b40' ,'#bdd576','#f6e67f' ,'#2db77f' ,'#61c6c0' ,'#61cbe8' ,'#d87fae' ,'#9772a3' ,'#1f6585' ,'#b6517f' ,'#a89778' ,'#eae4b1' ,'#a2a9ad' ,'#a65b4a' ,'#82766a' ,'#797c82']
metabolic_colors_40 = ['#a63246' ,'#cd3e49' ,'#e56e61' ,'#d16d29' ,'#ea9243' ,'#d8a83b' ,'#ffc840' ,'#5f8943' ,'#789b40' ,'#87bf65' ,'#bdd576' ,'#e2e26a' ,'#f6e67f' ,'#288e5b' ,'#2db77f' ,'#43a89a' ,'#61c6c0' ,'#a9dde3' ,'#61cbe8' ,'#60adcd' ,'#d87fae' ,'#a4a9d5' ,'#9772a3' ,'#775285' ,'#1f6585' ,'#2e839e' ,'#b6517f' ,'#a09256' ,'#a89778' ,'#c4b36a' ,'#eae4b1' ,'#f5f3ea' ,'#a2a9ad' ,'#b7744f' ,'#a65b4a' ,'#7b5d52' ,'#82766a' ,'#8c9380' ,'#797c82']


def pie_chart(df,gp_bin = False, gp='HICL',topn=0,
              value = 'Net Weight Received'):
  if gp_bin:
     df = df.groupby(gp).sum().reset_index().sort_values(value,ascending=False)
  if topn:
     df = df.iloc[0:topn,:]
  fig_pie = go.Figure(data=[
      go.Pie(labels=df[gp], values=df[value],
             marker=dict(colors=metabolic_colors_20))
      ])
  fig_pie.update_traces(textposition='inside', textinfo='text+value+label',
                        hoverinfo='label+value+percent')
  return(fig_pie)



# url_df = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={df_id}"
# url_match = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={lookup_id}"
# url_df_fig_in = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={df_fig_in_id}"

# print(url_df_fig_in)
# df_RA_final_HICL_splitCountry = pd.read_csv(url_df_fig_in)

WORK_SHEET_NAME = 'Included_Ingredients'

# build connection and load google spreadsheet as dataframe
conn2 = st.connection("gsheets2",type=GSheetsConnection)
df_RA_final_HICL_splitCountry = conn2.read(worksheet=WORK_SHEET_NAME)

# show the first 5 lines of the loaded datatrame
with st.expander('USfood data frame (Included_Ingredients): '):
       st.dataframe(df_RA_final_HICL_splitCountry.head())

cols = ['HICL','Merch Category','PIM Group','Net Weight Received (lb)',
        'Country of Origin','Product Description']


df = df_RA_final_HICL_splitCountry.loc[:,cols]
df = df.loc[(df['HICL'].notnull())&(df['HICL']!=''),:]



# all HICL categories pie & bar chart
st.header("Net Weight Received - All HICL")
df_hicl_fig = df.groupby('HICL').sum().reset_index().sort_values('Net Weight Received (lb)',ascending=False)

st.subheader('Bar plot: Net Weight Received - All HICL',divider='gray')
fig_hicl_bar = px.bar(df_hicl_fig,
                x='HICL', y='Net Weight Received (lb)',
                )
fig_hicl_bar.update_xaxes(tickangle=75)
fig_hicl_bar.update_traces(marker_color='#b52451')
st.plotly_chart(fig_hicl_bar, use_container_width=True)
st.write("  \n")

st.subheader('Pie plot: Net Weight Received - All HICL',divider='gray')
fig_hicl_pie = pie_chart(df_hicl_fig,gp_bin=False,gp='HICL',value='Net Weight Received (lb)')
fig_hicl_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
st.plotly_chart(fig_hicl_pie, use_container_width=True)
st.write("  \n")
st.write("  \n")


# breakdown HICL- PIM Group and Merch Category
st.header("Breakdwon HICL into PIM Group & Merch Category")
select_list = st.multiselect(
    'select HICL',
    df['HICL'].unique().tolist(),
    ['Poultry'])
df_select = df.loc[df['HICL'].isin(select_list),:]

# PIM/merch/product counting in each HICL: summary dataframe
df_count = pd.DataFrame()
df_count.index = select_list
for h in select_list:
   df_count.loc[h,'PIM group numbers'] = len(df_select.loc[df_select['HICL']==h,'PIM Group'].unique())
   df_count.loc[h,'Merch category numbers'] = len(df_select.loc[df_select['HICL']==h,'Merch Category'].unique())
   df_count.loc[h,'Products numbers'] = len(df_select.loc[df_select['HICL']==h,'Product Description'].unique())
st.dataframe(df_count)

# breakdown pie plot
for i in ['PIM Group','Merch Category']:
    st.subheader(f"Breakdwon HICL into {i}, top 20 ingredients",divider='grey')
    fig_select_pie = pie_chart(df_select,gp_bin=True,gp=i,
                            topn=20,value='Net Weight Received (lb)')
    fig_select_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_select_pie, use_container_width=True)
    st.write("  \n")



    