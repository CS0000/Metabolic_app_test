import streamlit as st
from annotated_text import annotated_text, annotation
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import folium
from streamlit_folium import st_folium
import pickle

st.set_page_config(layout="wide")
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

# load data
p = pd.read_csv('./Phase1_processed_dataset_pressures - Long_data_with_pressures_v2.csv')
test = p.loc[:,['Category_L4_LCA','Quantity', 'Land Use (m2)','Land Transformation (m2)','Water Use (m3)','Soil Pollution (kg SO2 eq)', 'Water Pollution (kg P eq)',]]


test1 = test.groupby(['Category_L4_LCA']).sum() # Harvest_Country
st.dataframe(test1.head(10))
test1_ra = test1.div(test1.sum(axis=0),axis=1).reset_index() 
all_C4 = test1.index.tolist()
all_col = test1.columns.tolist()

with open('./geo_country_new.plk','rb') as f:
    l = pickle.load(f)

class pressureHome:
    def __init__(self,path):
        self.path = path
        self.df = pd.read_csv(self.path)

    def sliceCol(self, col = []):
        self.df = self.df.loc[:,col]
        # return self.df
    
    def lookupCol(self,col=None):
        self.df_gb = self.df.groupby([col]).sum()
        self.df_gb_ra = self.df_gb.div(self.df_gb.sum(axis=0),axis=1).reset_index() 
    
        
