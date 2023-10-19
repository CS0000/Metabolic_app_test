from helper import *
from folium import Popup
import plotly.express as px
import streamlit as st


st.set_page_config(layout="wide")
st.header('this is map view page')
@st.cache(allow_output_mutation=True)

def base_map():
    m = folium.Map(tiles='OpenStreetMap', 
                   location=[41.38716817075619, 2.170044811509568],
                   zoom_start=2)
    return m


# html file for the node on the map
def plotly_graph():
    categories = ['A', 'B', 'C']
    values = [10, 20, 15]
    fig = px.bar(x=categories, y=values, title="Sample Bar Plot")
    fig.write_html('./test.html')

# html -> folium popup
def plotly_foPop():
    # base map
    with open('./test.html','r') as f:
        html = f.read()
    iframe = folium.IFrame(html=html,width=300,height=200)
    popup = Popup(iframe,max_width=300)
    # folium.Marker([30,110],popup=popup).add_to(m)
    # st.session_state['map_created'] = True
    return popup


def main():
    if 'm' not in st.session_state:
        st.session_state.m = base_map()
        # popup = plotly_foPop()
        # folium.Marker([30,110],popup=popup).add_to(st.session_state.m)
        st_folium(st.session_state.m,use_container_width=True)
        st.session_state.m = True
    else:
        st_folium(base_map(),use_container_width=True)

if __name__ == '__main__':
    main()

# e = st.container()
# m = base_map()
# popup = plotly_foPop()
# folium.Marker([30,110],popup=popup).add_to(m)


    








# m = folium.Map(tiles='OpenStreetMap', location=[41.38716817075619, 2.170044811509568],zoom_start=2)
# for country in test['Harvest_Country'].unique():
#     lat,lon = l[country]['la'],l[country]['lon']
#     # popup = folium.Popup(html_plot, max_width=400)
#     folium.Marker([lat,lon],tooltip=country).add_to(m)

# # folium.Marker([30,94],tooltip='XXXXXXXChina').add_to(m)
# categories = ['A', 'B', 'C']
# values = [10, 20, 15]
# fig = px.bar(x=categories, y=values, title="Sample Bar Plot")
# fig.write_html('./test.html')

# html="""
#     <iframe src=\"""" + './test.html' + """\" width="850" height="400"  frameborder="0">    
#     """
# popup = folium.Popup(html='./test.html', max_width=400)
# iframe = folium.IFrame(html=open('./test.html','r').read(),width=400,height=300)
# popup = folium.Popup(folium.Html(iframe))
# # folium.Marker([30,110],tooltip='XXXXXXXChina',popup=popup).add_to(m)

# d = st_folium(m, use_container_width=True)# height=700)# use_container_width=True)

