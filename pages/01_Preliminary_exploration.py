from helper import *
import plotly.express as px
# from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.header('Data exploration')

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



# WORK_SHEET_NAME = 'Included_Ingredients'
if 'df' not in st.session_state:
       st.warning("Please go back to Introduction page and locate to your dataset")
else:
       pressure = st.session_state.df
       with st.expander('Preview dataset'):
              st.dataframe(pressure.head())


       with st.form("Select columns for overall bar & pie plots"):
              index_col = st.selectbox(
                     'Which numerical column is going to be shown in the Y axis?',
                     pressure.columns.tolist())
              cate_col = st.selectbox(
                   'Which categorical column is going to be shown in the X axis?',
                   pressure.columns.tolist()
              )

              submitted = st.form_submit_button("Submit selection")
              if submitted:
                  st.header(f"{index_col} - {cate_col}")
                  df = pressure.loc[(pressure[cate_col].notnull())&(pressure[cate_col]!=''),:]
                  df_hicl_fig = df.groupby(cate_col).sum().reset_index().sort_values(index_col, ascending=False)

                  st.subheader(f'Bar plot: {index_col} - {cate_col}',divider='gray')
                  fig_hicl_bar = px.bar(df_hicl_fig,
                                 x=cate_col, y=index_col,
                                 )
                  fig_hicl_bar.update_xaxes(tickangle=75)
                  fig_hicl_bar.update_traces(marker_color='#b52451')
                  st.plotly_chart(fig_hicl_bar, use_container_width=True)

                  st.subheader(f'Pie plot: {index_col} - {cate_col}',divider='gray')
                  fig_hicl_pie = pie_chart(df_hicl_fig,gp_bin=False,gp=cate_col,value=index_col)
                  fig_hicl_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                  st.plotly_chart(fig_hicl_pie, use_container_width=True)
                  st.write("  \n")
                  st.write("  \n")

       with st.form("Select columns for breakdown pie plots"):
            # breakdown HICL- PIM Group and Merch Category
            index_col = st.selectbox(
                     'Which numerical column is going to be shown in the Y axis?',
                     pressure.columns.tolist())
            cate_col = st.selectbox(
                     'Which categorical column is going to be breakdown?',
                     pressure.columns.tolist())
            break_cate_col = st.selectbox(
                     'Which categorical column is going to be shown in the X axis?',
                     pressure.columns.tolist())
         

            # df = pressure.loc[(pressure[cate_col].notnull())&(pressure[cate_col]!=''),:]
            # select_list = st.multiselect(
            #    f'select {cate_col}',
            #    pressure[cate_col].unique().tolist(),
            #    pressure[cate_col].unique().tolist()[0])
            # df_select = pressure.loc[pressure[cate_col].isin(select_list),:]

            # breakdown pie plot
            

            submitted = st.form_submit_button("Submit selection")
            if submitted:
                  st.header(f"Breakdwon {cate_col} into {break_cate_col}")
                  n = st.slider('show top N ingredients: ', 1,20,10)
                  st.subheader(f"Breakdwon {cate_col} into {break_cate_col}, top {n} ingredients",divider='grey')

                  select_list = st.multiselect(
                     f'select {cate_col}',
                     pressure[cate_col].unique().tolist(),
                     pressure[cate_col].unique().tolist()[0])
                  st.info("click Submit bottom to renew if the selections are changed above")
                  df_select = pressure.loc[pressure[cate_col].isin(select_list),:]
                  fig_select_pie = pie_chart(df_select,gp_bin=True,gp=break_cate_col,
                                          topn=n,value=index_col)
                  fig_select_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                  st.plotly_chart(fig_select_pie, use_container_width=True)
                  st.write("  \n")
            
            





# # breakdown HICL- PIM Group and Merch Category
# st.header("Breakdwon HICL into PIM Group & Merch Category")
# select_list = st.multiselect(
#     'select HICL',
#     df['HICL'].unique().tolist(),
#     ['Poultry'])
# df_select = df.loc[df['HICL'].isin(select_list),:]

# # PIM/merch/product counting in each HICL: summary dataframe
# df_count = pd.DataFrame()
# df_count.index = select_list
# for h in select_list:
#    df_count.loc[h,'PIM group numbers'] = len(df_select.loc[df_select['HICL']==h,'PIM Group'].unique())
#    df_count.loc[h,'Merch category numbers'] = len(df_select.loc[df_select['HICL']==h,'Merch Category'].unique())
#    df_count.loc[h,'Products numbers'] = len(df_select.loc[df_select['HICL']==h,'Product Description'].unique())
# st.dataframe(df_count)

# # breakdown pie plot
# for i in ['PIM Group','Merch Category']:
#     st.subheader(f"Breakdwon HICL into {i}, top 20 ingredients",divider='grey')
#     fig_select_pie = pie_chart(df_select,gp_bin=True,gp=i,
#                             topn=20,value='Net Weight Received (lb)')
#     fig_select_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
#     st.plotly_chart(fig_select_pie, use_container_width=True)
#     st.write("  \n")



    