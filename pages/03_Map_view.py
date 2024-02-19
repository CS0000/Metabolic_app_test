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




st.set_page_config(layout="wide")
st.header('Map view')

metabolic_colors_20 = ['#a63246' ,'#e56e61' ,'#ea9243' ,'#ffc840' ,'#789b40' ,'#bdd576','#f6e67f' ,'#2db77f' ,'#61c6c0' ,'#61cbe8' ,'#d87fae' ,'#9772a3' ,'#1f6585' ,'#b6517f' ,'#a89778' ,'#eae4b1' ,'#a2a9ad' ,'#a65b4a' ,'#82766a' ,'#797c82']
metabolic_colors_40 = ['#a63246' ,'#cd3e49' ,'#e56e61' ,'#d16d29' ,'#ea9243' ,'#d8a83b' ,'#ffc840' ,'#5f8943' ,'#789b40' ,'#87bf65' ,'#bdd576' ,'#e2e26a' ,'#f6e67f' ,'#288e5b' ,'#2db77f' ,'#43a89a' ,'#61c6c0' ,'#a9dde3' ,'#61cbe8' ,'#60adcd' ,'#d87fae' ,'#a4a9d5' ,'#9772a3' ,'#775285' ,'#1f6585' ,'#2e839e' ,'#b6517f' ,'#a09256' ,'#a89778' ,'#c4b36a' ,'#eae4b1' ,'#f5f3ea' ,'#a2a9ad' ,'#b7744f' ,'#a65b4a' ,'#7b5d52' ,'#82766a' ,'#8c9380' ,'#797c82']
c = metabolic_colors_40 + metabolic_colors_20

if 'df' not in st.session_state:
       st.warning("Please go back to Introduction page and locate to your dataset")
else:
       df = st.session_state.df
       with st.expander('Preview dataset'):
              st.dataframe(df.head())

       with st.form("input"):
            country_col = st.selectbox("indicate the column for country names",
                                            df.columns.tolist())
            st.warning("If error raised after submitting, check whether the country column is correctly selected. ")
            st.image('./data/demo_map.png',output_format='PNG',
                     caption="expected output of global / local scale exploration")
            
            c1,c2 = st.columns(2) # st.columns([3, 1])
            with c1:
                st.write("Global scale")
                colored_col = st.selectbox("indicate the quantity/impacts/SoN",
                                              df.columns.tolist())
                st.text("summarize each country by sum or mean ?")
                func_groupby = st.selectbox("indicate sum or mean",
                                 ['sum','mean'])
                
            with c2:
                st.write("Local scale")
                local_impacts_col = st.multiselect("indicate the impacts shown in the pop-up window",df.columns.tolist())
                local_cate_col = st.selectbox("indicate the commodity category shown in the pop-up window",df.columns.tolist())

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
                    name=f'{colored_col}',
                    columns= [country_col,colored_col],
                    key_on="feature.properties.name",
                    fill_color= "RdYlGn_r",
                    line_opacity=0.3,
                    nan_fill_color='white',
                    legend_name=f'{colored_col}'
                ).add_to(m)
                


                # marker pop up
                cc = dict(zip(df[local_cate_col].unique(),c))
                if (len(local_impacts_col)!=0) and (len(local_cate_col)!=0):
                    fg_country = folium.FeatureGroup(name=f'Local scale view',show=False).add_to(m)
                    # st.dataframe(df_country.head(10))
                    for country in df_country[country_col].tolist():
                        la = df_country.loc[df_country[country_col]==country,'geo_center'].values[0][1]
                        lon = df_country.loc[df_country[country_col]==country,'geo_center'].values[0][0]

                        # x = np.arange(10)
                        # fig = go.Figure(data=[go.Scatter(x=x, y=x**2,line=dict(color='royalblue')),
                        #                     go.Scatter(x=x,y=x,line=dict(color='red'))])
                        # fig.update_layout(margin=dict(t=20,l=20,b=20,r=20))
                        
                        test = df.loc[df[country_col]==country,:]
                        for i in local_impacts_col:
                                test[i] = pd.to_numeric(test[i], errors='coerce')
                        test1 = test.groupby([local_cate_col]).sum() 
                        test1_ra = test1.div(test1.sum(axis=0),axis=1).reset_index()

                        bar_data = []
                        for ind,i in enumerate(test1_ra[local_cate_col].unique()):
                            bar_data.append(
                                    go.Bar(name=i, x=local_impacts_col,n = i * len(local_cate_col),
                                            y=test1_ra.loc[test1_ra[local_cate_col]==i,local_impacts_col].iloc[0,:].tolist(),
                                            marker_color = cc[i], # metabolic_colors_40[ind],
                                            hovertemplate = "%{n}: <br> %{x} </br> percentage: %{y} "
                                                    ))
                        fig = go.Figure(data = bar_data)
                        fig.update_layout(barmode='stack')
                        fig.update_layout(width=500,
                                    height=380,
                                    xaxis_title='',
                                    yaxis_title='%',
                                    font=dict(size=10),
                                    template=metabolic_template,
                                    title=f'{country}',
                                    legend_title_text=f'{local_cate_col}'
                                    # margin=dict(l=10, r=10, t=10, b=10)
                                    )
                        html = fig.to_html(include_plotlyjs='cdn')
                        iframe = branca.element.IFrame(html=html, width=500, height=300)
                        popup = folium.Popup(iframe, max_width=500)

                        if test1_ra.shape[0]>=1:
                            folium.Marker([la,lon], popup=popup).add_to(fg_country)
                # folium.Marker([30,10], popup='teset test').add_to(m)


                # x = np.arange(10)
                # fig = go.Figure(data=[go.Scatter(x=x, y=x**2,line=dict(color='royalblue')),
                #                       go.Scatter(x=x,y=x,line=dict(color='red'))])
                # fig.update_layout(margin=dict(t=20,l=20,b=20,r=20))
                # html = fig.to_html(include_plotlyjs='cdn')
                # iframe = branca.element.IFrame(html=html, width=500, height=300)
                # popup = folium.Popup(iframe, max_width=500)

                # folium.Marker([0,0], popup=popup,icon=folium.Icon(color='green')).add_to(m)

                folium.LayerControl().add_to(m)

                
                # st.warning("The points on the map only indicate the country's name for now. The pop up window of each point is still under development. Click the green point to see the demo of a possible content of pop up window. ")
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


