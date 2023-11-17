from helper import *
from st_ant_tree import st_ant_tree
import os

st.header('Diageo pressure data')
metabolic_colors_20 = ['#a63246' ,'#e56e61' ,'#ea9243' ,'#ffc840' ,'#789b40' ,'#bdd576','#f6e67f' ,'#2db77f' ,'#61c6c0' ,'#61cbe8' ,'#d87fae' ,'#9772a3' ,'#1f6585' ,'#b6517f' ,'#a89778' ,'#eae4b1' ,'#a2a9ad' ,'#a65b4a' ,'#82766a' ,'#797c82']
metabolic_colors_40 = ['#a63246' ,'#cd3e49' ,'#e56e61' ,'#d16d29' ,'#ea9243' ,'#d8a83b' ,'#ffc840' ,'#5f8943' ,'#789b40' ,'#87bf65' ,'#bdd576' ,'#e2e26a' ,'#f6e67f' ,'#288e5b' ,'#2db77f' ,'#43a89a' ,'#61c6c0' ,'#a9dde3' ,'#61cbe8' ,'#60adcd' ,'#d87fae' ,'#a4a9d5' ,'#9772a3' ,'#775285' ,'#1f6585' ,'#2e839e' ,'#b6517f' ,'#a09256' ,'#a89778' ,'#c4b36a' ,'#eae4b1' ,'#f5f3ea' ,'#a2a9ad' ,'#b7744f' ,'#a65b4a' ,'#7b5d52' ,'#82766a' ,'#8c9380' ,'#797c82']


SHEET_NAME = 'Phase1_pressures'
WORK_SHEET_NAME = 'Long_data_with_pressures'
SHEET_ID = 890331805

# pressure_url = 'https://docs.google.com/spreadsheets/d/1TPyl6dFr1rSBDuAHksywHxUJIUIaup94wIB2CJMh2xQ/edit#gid=890331805'
# sheet_name = 'Long_data_with_pressures'

cate_cols = ['Category_L1','Category_L2','Category_L3','Category_L4']
# index_cols: numerical, show in the bar x axis
index_cols = ['Converted crop weight (tonnes)', 
              'Global Warming Potential (kg CO2-Eq)', 'Air Pollution (kg PM2.5-Eq)',
              'Land Use (m2)', 'Water Pollution (kg P eq)',
              'Land Transformation (m2)', 'Soil Pollution (kg SO2 eq)',
              'Water Use (m3)']
final_col = f'{cate_cols[-1]}_Title'

# sheet_id = sheet_url_split(pressure_url)
# pressure = read_sheet(sheet_id,sheet_name)

# pressure = pd.read_csv('./pages/Phase1_pressures - Long_data_with_pressures.csv')

# pressure = read_credentials_sheet(SHEET_NAME,SHEET_ID)

conn1 = st.connection("gsheets1",type=GSheetsConnection)
pressure = conn1.read(worksheet=WORK_SHEET_NAME)


with st.expander('pressure data frame: '):
       st.dataframe(pressure.head())

# tree data accroding to cate_cols
tree_data, tree_data_df = build_tree(pressure,0,len(cate_cols))
tree_data_df = tree_data_df.loc[:,[i for i in tree_data_df.columns.tolist() if i not in cate_cols]]
pressure_new = pd.concat([tree_data_df,pressure],axis=1)
# st.dataframe(pressure_new.head())


with st.container():
       value = st_ant_tree(treeData=tree_data, filterTreeNode= True, 
                     allowClear=True, max_height=700,min_height_dropdown=120,
                     multiple= True, placeholder= "filtering categories", 
                     showArrow= True, showSearch= True, treeCheckable= True)


# st.write(value) # value: list : ['leaf1', 'leaf2', 'leaf3']
on = st.toggle('bar summing up = 100%')

if value:
    if on:
       # st.dataframe(pressure_new.loc[pressure_new[final_col].isin(value),:])
       test = pressure_new.loc[pressure_new[final_col].isin(value),:]
       for i in index_cols:
              test[i] = pd.to_numeric(test[i], errors='coerce')
       test1 = test.groupby([final_col]).sum() 
       test1_ra = test1.div(test1.sum(axis=0),axis=1).reset_index() 

    else:
       test = pressure_new.copy()
       for i in index_cols:
             test[i] = pd.to_numeric(test[i], errors='coerce')
       test = test.groupby([final_col]).sum()
       test1 = test.div(test.sum(axis=0),axis=1).reset_index() 
       test1_ra = test1.loc[test1[final_col].isin(value),:]
    
    # matching long and short name for the last category
    match_df = pressure_new.loc[pressure_new[final_col].isin(value),
                                   [cate_cols[-1],final_col]]
    match_df = match_df.drop_duplicates()
    bare_name_d = dict(zip(match_df[final_col].tolist(),
                           match_df[cate_cols[-1]].tolist()))
    bar_data = []
    for ind,i in enumerate(value):
            bar_data.append(
                  go.Bar(name=bare_name_d[i], x=index_cols, 
                         y=test1_ra.loc[test1_ra[final_col]==i,index_cols].iloc[0,:].tolist(),
                         marker_color = metabolic_colors_40[ind]
                                ))

    fig = go.Figure(data = bar_data)
    fig.update_layout(barmode='stack')
    fig.update_layout(width=800,
                    height=800,
                    xaxis_title='',
                    yaxis_title='%',
                    template=metabolic_template,
                    margin=dict(l=10, r=10, t=10, b=10)
                    # name='My Legend Name'
                    )

    st.plotly_chart(fig, use_container_width=True)

