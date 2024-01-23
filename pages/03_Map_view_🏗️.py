from helper import *
from folium import Popup
import plotly.express as px
# import vincent
import streamlit as st
import requests
import numpy as np
# from altair import *
from shapely.geometry import shape
import branca
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload



st.set_page_config(layout="wide")
st.header('Map view')

if 'df' not in st.session_state:
       st.warning("Please go back to Introduction page and locate to your dataset")
else:
       df = st.session_state.df
       with st.expander('Preview dataset'):
              st.dataframe(df.head())
    #    with st.form('form'):
    #           country_col = st.selectbox("indicate the column for country names",
    #                                      df.columns.tolist())
    #           colored_col = st.selectbox("indicate the column for numerical colors",
    #                                      df.columns.tolist())
              
    #           submitted = st.form_submit_button("Submit selection")

       with st.form("input"):
            st.write("locate to your data:")
            c1,c2 = st.columns(2) # st.columns([3, 1])
            with c1:
                country_col = st.selectbox("indicate the column for country names",
                                            df.columns.tolist())
            with c2:
                colored_col = st.selectbox("indicate the numerical column for coloring",
                                            df.columns.tolist())
                st.text("summarize each country by sum or mean ?")
                func_groupby = st.selectbox("indicate sum or mean",
                                 ['sum','mean'])

            # with c4:
            #      x2 = st.selectbox("indicate the column for numerical colors",
            #                                 df.columns.tolist())
            st.warning("If error raised after submitting, check whether the country column is correct. ")
            submitted = st.form_submit_button("Submit")

            if submitted:
                # load country ploygons geojson
                political_countries_url = ("http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson")
                data = requests.get(political_countries_url).json()
                db_country_names = {} # {'country_name':[],'geo':[],'geo_center':[]}
                for i in data['features']:
                    k = i['properties']['name']
                    _ = shape(i['geometry']).centroid
                    db_country_names[k] = {'geo':i['geometry']['coordinates'],
                                           'geo_center':[_.x, _.y]}

                    
                # df_country
                df_country = df.loc[:,[country_col,colored_col]]
                df_country[colored_col] = df[colored_col].apply(pd.to_numeric, errors='coerce')
                if func_groupby == 'sum':
                    df_country = df_country.groupby([country_col]).sum()
                if func_groupby == 'mean':
                    df_country = df_country.groupby([country_col]).mean()
                else:
                    df_country = df_country.groupby([country_col]).sum() # default is sum
                df_country = df_country.reset_index()
                # adjust country name for df_country
                country_ = []
                for i in df_country[country_col].tolist():
                    if i== "Cote d'Ivoire":
                        i_ = "Côte d'Ivoire"
                    elif i == 'Czech Republic':
                        i_ = 'Czech Rep.'
                    elif i == 'Dominican Republic':
                        i_ = 'Dominican Rep.'
                    elif i == 'South Korea':
                        i_ = 'Korea'
                    elif i == 'Türkiye':
                        i_ = 'Turkey'
                    else:
                        i_ = i
                    country_.append(i_)
                df_country[country_col] = country_
                _ = ''
                for i in df_country[country_col].tolist():
                    if i not in db_country_names:
                        _ = i + ', '
                if len(_) != 0:
                    st.warning(f"not standardized country name: {_}")
                
                # add geo_center column
                df_country['geo_center'] = df_country[country_col].apply(lambda x: db_country_names[x]['geo_center'])
                # st.dataframe(df_country.head())

                m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
                # folium.GeoJson(political_countries_url).add_to(m)
                
                folium.Choropleth(
                    geo_data=political_countries_url,
                    data=df_country,
                    columns= [country_col,colored_col],
                    key_on="feature.properties.name",
                    fill_color= "RdYlGn_r",
                    line_opacity=0.3,
                    nan_fill_color='white',
                    legend_name=f'{colored_col}'
                ).add_to(m)
                
                # marker pop up
                fg_country = folium.FeatureGroup(name=f'country level of {colored_col}',show=False).add_to(m)
                for i in df_country[country_col].tolist():
                    la = df_country.loc[df_country[country_col]==i,'geo_center'].values[0][1]
                    lon = df_country.loc[df_country[country_col]==i,'geo_center'].values[0][0]
                    folium.Marker([la,lon], popup=i).add_to(fg_country)
                # folium.Marker([30,10], popup='teset test').add_to(m)


                x = np.arange(10)
                fig = go.Figure(data=[go.Scatter(x=x, y=x**2,line=dict(color='royalblue')),
                                      go.Scatter(x=x,y=x,line=dict(color='red'))])
                # df = px.data.gapminder().query("continent=='Oceania'")
                # fig = px.line(df, x="year", y="lifeExp", color='country')
                fig.update_layout(margin=dict(t=20,l=20,b=20,r=20))
                    
                html = fig.to_html(include_plotlyjs='cdn')
                iframe = branca.element.IFrame(html=html, width=500, height=300)
                popup = folium.Popup(iframe, max_width=500)

                folium.Marker([0,0], popup=popup,icon=folium.Icon(color='green')).add_to(m)

                folium.LayerControl().add_to(m)

                
                st.warning("The points on the map only indicate the country's name for now. The pop up window of each point is still under development. Click the green point to see the demo of a possible content of pop up window. ")
                st_data = st_folium(m,width=1200,height=1000)


            
                     
              















       
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


