from helper import *
from folium import Popup
import plotly.express as px
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import geopandas as gpd
# import fiona, tempfile
import pickle,io
import pydeck as pdk

st.set_page_config(layout="wide")
st.header('this is map view page')

@st.cache_resource
def drive_client():
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], 
        # scopes=["https://www.googleapis.com/auth/drive.readonly"])
        scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file'])
    return build('drive', 'v3', credentials=creds)


@st.cache_data
def load_from_drive(file_id):
    service = drive_client()
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh,request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    fh.seek(0)
    return fh


data_load_state = st.text('Loading data...') 
pickle_geojson_id = '1AZDR2F2vrBfw-f-l07Av-g1iXlz2alpG'
fh = load_from_drive(pickle_geojson_id)

data = pickle.load(fh)
data_load_state.text('Loading data... done!')



def gerate_map(data):
    m = folium.Map(zoom_start=3)
    folium.GeoJson(data).add_to(m)
    # data_load_state.text('map object m done')
    st_folium(m,width=1200,height=700,zoom=8)

with st.form(key='sss'):
    gerate_map(data)
    submitted = st.form_submit_button("show map parameters")
    if submitted:
       st.write('map para')










       
# view_state = pdk.ViewState(latitude=38,longitude=-122,zoom=3)
# layer = pdk.Layer(
#     "GeoJsonLayer",
#     data=data,
#     opacity=0.8,
#     stroked=False,
#     filled=True,
#     extruded=False,
#     get_line_color=[255,255,255]
# )

# st.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9", 
#                          layers=[layer], 
#                          initial_view_state=view_state))



# https://drive.google.com/file/d/1AZDR2F2vrBfw-f-l07Av-g1iXlz2alpG/view?usp=sharing








# file_id_shx = '1b-Gra1JVjxePqMzHCC7jyPyzcIY7GSc8'
# file_id_shp = '1b2hAU5YNtWFZ6xiPBscqcyxw0Eb0d1ZH'  # Replace with your file ID
# file_id_dbf = '1b4fDqoJW5Od_FgmoHEfZAa1duwdDf7Dt'
# gdf = load_shape_file(file_id_shp,file_id_shx,file_id_dbf, service)
# st.write('downloaded')


# gdf['geometry'] = gdf['geometry'].simplify(0.01)
# geo_json_simp = gdf.to_json()
# st.write('tranformed to json and simplified')

# m = folium.Map()
# st.write('get map')

# folium.GeoJson(geo_json_simp,name='geojson').add_to(m)
# st.write('json to map')


