import streamlit as st
from annotated_text import annotated_text, annotation
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import folium
from streamlit_folium import st_folium
import pickle
import gspread 
import json
from streamlit_gsheets import GSheetsConnection



color_map = {'Agave': '#d5de81',
             'Aniseed': '#CCAB62',
             'Barley':'#fccb7d',
             'Berries':'#e5504c',
             'Broken Rice':'#fba2bc',
             'Cocoa':'#A57463',
             'Coffee':'#8c6f42',
             'Grapes':'#a8b240',
             'Hops':'#2eaf62',
             'Juniper':'#b75334',
             'Lemon/Lime':'#f7d64d',
             'Liquorice':'#8181EA',
             'Maize':'#f9ae41',
             'Milk':'#d8b9b0',
             'Rye':'#f97c50',
             'Sorghum':'#d64973',
             'Sugarbeet':'#fcab87',
             'Sugarcane':'#6ad9e3',
             'Vanilla':'#f29392',
             'Wheat':'#3590db',
             'Broken Rice (GNS)':'#ffd7d7',
             'Sugarcane (GNS)':'#48ccb2',
             'Maize (GNS)':'#fff19f',
             'Wheat (GNS)':'#cae6ff',
             'Flavours':' #8181EA'
             }
metabolic_template = dict(layout=go.Layout(font_family='Roboto',
                                           font_color='#575757',
                                           autosize=True,
                                           xaxis_title=None,
                                           yaxis={'categoryorder': 'sum descending'},
                                           title=dict(
                                                      font=dict(size = 25),
                                                      xref='paper',
                                                      yref='paper',
                                                      ),
                                           font=dict(size=18),
                                           xaxis=dict(automargin=True),
                                           ))
metabolic_colors_20 = ['#a63246' ,'#e56e61' ,'#ea9243' ,'#ffc840' ,'#789b40' ,'#bdd576','#f6e67f' ,'#2db77f' ,'#61c6c0' ,'#61cbe8' ,'#d87fae' ,'#9772a3' ,'#1f6585' ,'#b6517f' ,'#a89778' ,'#eae4b1' ,'#a2a9ad' ,'#a65b4a' ,'#82766a' ,'#797c82']
metabolic_colors_40 = ['#a63246' ,'#cd3e49' ,'#e56e61' ,'#d16d29' ,'#ea9243' ,'#d8a83b' ,'#ffc840' ,'#5f8943' ,'#789b40' ,'#87bf65' ,'#bdd576' ,'#e2e26a' ,'#f6e67f' ,'#288e5b' ,'#2db77f' ,'#43a89a' ,'#61c6c0' ,'#a9dde3' ,'#61cbe8' ,'#60adcd' ,'#d87fae' ,'#a4a9d5' ,'#9772a3' ,'#775285' ,'#1f6585' ,'#2e839e' ,'#b6517f' ,'#a09256' ,'#a89778' ,'#c4b36a' ,'#eae4b1' ,'#f5f3ea' ,'#a2a9ad' ,'#b7744f' ,'#a65b4a' ,'#7b5d52' ,'#82766a' ,'#8c9380' ,'#797c82']



def df_input_form():
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
    return C1,C2,submitted

# for local testing only
cred_path = './credentials.json'
@st.cache_resource()
def get_google_sheet_connection(sheet_name):
    with open(cred_path) as j_f:
        cred = json.load(j_f)
    gc, authorized_user = gspread.oauth_from_dict(cred)
    sh = gc.open(sheet_name)  # spreadsheet name  "Phase1_pressures"
    return sh

@st.cache_data()
def read_credentials_sheet(sheet_name, worksheet_id):
    sh = get_google_sheet_connection(sheet_name)
    worksheet = sh.get_worksheet_by_id(worksheet_id) # #gid sheet_id 890331805
    data = worksheet.get_all_values()
    df = pd.DataFrame(data)
    df.columns = df.iloc[0] 
    df = df[1:] 
    return df


# cate_cols = ['Category_L1', 'Category_L2', 'Category_L3', 'Category_L4']
# def build_tree(df, current_level, max_level, path='', new_df=None):
#     if current_level == 0:
#         # Initialize the new DataFrame with the same index as the original
#         new_df = pd.DataFrame(index=df.index)
    
#     if current_level >= max_level:
#         return [], new_df

#     next_level = current_level + 1
#     tree = []

#     category_col = f'Category_L{current_level + 1}'
#     title_col = f'{category_col}_Title'

#     for index, item in enumerate(df[cate_cols[current_level]].unique()):
#         if pd.notna(item):
#             # Create a path label with leading numbers
#             new_path = f'{path}{index:02d}_'

#             # Filter the DataFrame for the current category item
#             filtered_df = df[df[cate_cols[current_level]] == item]
            
#             # Recursive call to build children and update new DataFrame
#             children, new_df = build_tree(filtered_df, next_level, max_level, new_path, new_df)

#             # Add category and title information to the new DataFrame
#             new_df.loc[filtered_df.index, category_col] = item
#             new_df.loc[filtered_df.index, title_col] = f'{new_path}{item} ({cate_cols[current_level]})'

#             node = {
#                 'value': f'{new_path}{item} ({cate_cols[current_level]})',
#                 'title': item,
#                 'children': children
#             }
#             if not node['children']:
#                 del node['children']
#             tree.append(node)

#     return tree, new_df



    
        
