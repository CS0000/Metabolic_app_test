from helper import *
from st_ant_tree import st_ant_tree
import os

st.header('Pressure data visualization')
metabolic_colors_20 = ['#a63246' ,'#e56e61' ,'#ea9243' ,'#ffc840' ,'#789b40' ,'#bdd576','#f6e67f' ,'#2db77f' ,'#61c6c0' ,'#61cbe8' ,'#d87fae' ,'#9772a3' ,'#1f6585' ,'#b6517f' ,'#a89778' ,'#eae4b1' ,'#a2a9ad' ,'#a65b4a' ,'#82766a' ,'#797c82']
metabolic_colors_40 = ['#a63246' ,'#cd3e49' ,'#e56e61' ,'#d16d29' ,'#ea9243' ,'#d8a83b' ,'#ffc840' ,'#5f8943' ,'#789b40' ,'#87bf65' ,'#bdd576' ,'#e2e26a' ,'#f6e67f' ,'#288e5b' ,'#2db77f' ,'#43a89a' ,'#61c6c0' ,'#a9dde3' ,'#61cbe8' ,'#60adcd' ,'#d87fae' ,'#a4a9d5' ,'#9772a3' ,'#775285' ,'#1f6585' ,'#2e839e' ,'#b6517f' ,'#a09256' ,'#a89778' ,'#c4b36a' ,'#eae4b1' ,'#f5f3ea' ,'#a2a9ad' ,'#b7744f' ,'#a65b4a' ,'#7b5d52' ,'#82766a' ,'#8c9380' ,'#797c82']


# SHEET_CODE = 'gsheets1'
# WORK_SHEET_NAME = 'Long_data_with_pressures'
procede = False

with st.form("input"):
       st.write("locate to your data:")
       c1, c2 = st.columns(2)
       with c1:
              C1 = st.text_input('Please enter the unique sheet code', '')
       with c2:
              C2 = st.text_input('Please enter the work sheet name', '')
       # SHEET_CODE = st.text_input('Please enter the unique sheet code', '')
       # WORK_SHEET_NAME  = st.text_input('Please enter the work sheet name', '')
       submitted = st.form_submit_button("Submit")

if (len(C1)!=0)&(len(C2)!=0):
       procede = True
       st.info("Submitted!")
else:
       procede = False 


# st.write('The current unique sheet code is ', work_sheet_name)
# pressure_url = 'https://docs.google.com/spreadsheets/d/1TPyl6dFr1rSBDuAHksywHxUJIUIaup94wIB2CJMh2xQ/edit#gid=890331805'
# sheet_name = 'Long_data_with_pressures'

# cate_cols = ['Category_L1','Category_L2','Category_L3','Category_L4']
# # index_cols: numerical, show in the bar x axis
# index_cols = ['Converted crop weight (tonnes)', 
#               'Global Warming Potential (kg CO2-Eq)', 'Air Pollution (kg PM2.5-Eq)',
#               'Land Use (m2)', 'Water Pollution (kg P eq)',
#               'Land Transformation (m2)', 'Soil Pollution (kg SO2 eq)',
#               'Water Use (m3)']
# final_col = f'{cate_cols[-1]}_Title'


if procede == True:
       try:
              SHEET_CODE, WORK_SHEET_NAME = C1,C2
              conn1 = st.connection(SHEET_CODE,type=GSheetsConnection)
              pressure = conn1.read(worksheet=WORK_SHEET_NAME)


              with st.expander('Preview pressure data'):
                     st.dataframe(pressure.head())


              with st.expander("Selecting columns"):
                     index_cols = st.multiselect(
                            'Which columns are going to be indexes shown in the X axis?',
                            pressure.columns.tolist())

                     cate_cols = st.multiselect(
                     "Multiple columns selection here. \
                     There will be tree-structrued filtering based on your selection. Make sure the selections are ordered. \
                     e.g. L1, L2, L3 (L1 is the largest category while L3 is the most detailed)",
                     pressure.columns.tolist()
                     )


              value = None

              if cate_cols:

                     # whatever the input columns are, tranform into Category_L1, Category_L2,... Category_Ln in order
                     cate_cols_alter = [f'category_L{i+1}' for i,k in enumerate(cate_cols)]
                     cate_cols_dict = {k:f'category_L{i+1}' for i,k in enumerate(cate_cols)}
                     pressure_ = pressure.copy()
                     alter_cols = []
                     for i in pressure_.columns.tolist():
                            if i in cate_cols:
                                   i_ = cate_cols_dict[i]
                            else:
                                   i_ = i
                            alter_cols.append(i_)
                     pressure_.columns = alter_cols

                     final_col = f'{cate_cols_alter[-1]}_Title'

                     def build_tree(df, current_level, max_level, path='', new_df=None):
                            if current_level == 0:
                                   # Initialize the new DataFrame with the same index as the original
                                   new_df = pd.DataFrame(index=df.index)
                            
                            if current_level >= max_level:
                                   return [], new_df

                            next_level = current_level + 1
                            tree = []

                            category_col = f'category_L{current_level + 1}'
                            title_col = f'{category_col}_Title'

                            for index, item in enumerate(df[cate_cols_alter[current_level]].unique()):
                                   if pd.notna(item):
                                          # Create a path label with leading numbers
                                          new_path = f'{path}{index:02d}_'

                                          # Filter the DataFrame for the current category item
                                          filtered_df = df[df[cate_cols_alter[current_level]] == item]
                                          
                                          # Recursive call to build children and update new DataFrame
                                          children, new_df = build_tree(filtered_df, next_level, max_level, new_path, new_df)

                                          # Add category and title information to the new DataFrame
                                          new_df.loc[filtered_df.index, category_col] = item
                                          new_df.loc[filtered_df.index, title_col] = f'{new_path}{item} ({cate_cols_alter[current_level]})'

                                          node = {
                                                 'value': f'{new_path}{item} ({cate_cols_alter[current_level]})',
                                                 'title': item,
                                                 'children': children
                                          }
                                          if not node['children']:
                                                 del node['children']
                                          tree.append(node)

                            return tree, new_df
                     
                     # # tree data accroding to cate_cols
                     # tree_data, tree_data_df = build_tree(pressure_,0,len(cate_cols_alter))
                     # tree_data_df = tree_data_df.loc[:,[i for i in tree_data_df.columns.tolist() if i not in cate_cols_alter]]
                     # # st.dataframe(tree_data_df.head())
                     # pressure_new = pd.concat([tree_data_df,pressure],axis=1)
                     # # st.dataframe(pressure_new.head())


                     with st.container():
                            cate_col_str = ''
                            for i in cate_cols:
                                   cate_col_str += '  ' + i 

                            # tree data accroding to cate_cols
                            tree_data, tree_data_df = build_tree(pressure_,0,len(cate_cols_alter))
                            tree_data_df = tree_data_df.loc[:,[i for i in tree_data_df.columns.tolist() if i not in cate_cols_alter]]
                            # st.dataframe(tree_data_df.head())
                            pressure_new = pd.concat([tree_data_df,pressure],axis=1)
                            # st.dataframe(pressure_new.head())

                            annotated_text(("Clear the filtering before reselecting the above","","#fea"))
                            # st.write("Clear the filtering before reselecting the above")
                            value = st_ant_tree(treeData=tree_data, filterTreeNode= True, 
                                          allowClear=True, max_height=700,min_height_dropdown=120,
                                          multiple= True, placeholder= "filtering categories", 
                                          showArrow= True, showSearch= True, treeCheckable= True)


                     # st.write(value) # value: list : ['leaf1', 'leaf2', 'leaf3']

              on = st.toggle('bar summing up = 100%')
              if value:
                     # st.write(
                     #        "indexes in X axis: ", index_cols,
                     #        "colored columns: ", cate_cols, cate_cols_alter)
                     # st.dataframe(pressure_new.head())
                     if on:
                            # st.dataframe(pressure_new.loc[pressure_new[final_col].isin(value),:])
                            test = pressure_new.loc[pressure_new[final_col].isin(value),:]
                            for i in index_cols:
                                   test[i] = pd.to_numeric(test[i], errors='coerce')
                            test1 = test.groupby([final_col]).sum() 
                            test1_ra = test1.div(test1.sum(axis=0),axis=1).reset_index() 

                     else:
                            test = pressure_new.copy()
                            # st.dataframe(test.head())
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

       except ValueError:
              st.error('Please enter a valid input')

else:
       pass