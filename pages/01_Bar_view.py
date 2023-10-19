from helper import *


st.header('this is overview page')


bar_data = []
C4_in = [] # ['Agave','Aniseed','Barley','Berries','Broken Rice']
col_in = [] # ['Quantity','Land Use (m2)','Land Transformation (m2)']

C4_in = st.sidebar.multiselect(
    'Select Categoriy_L4',
    all_C4,
    all_C4)

col_in = st.sidebar.multiselect(
    'Select index',
    all_col,
    all_col)

for i in C4_in:
        bar_data.append(go.Bar(name=i, x=col_in, 
                            y=test1_ra.loc[test1_ra['Category_L4_LCA']==i,col_in].iloc[0,:].tolist(),
                            marker_color = color_map[i]
                            ))

fig = go.Figure(data = bar_data)
fig.update_layout(barmode='stack'
                )
fig.update_layout(width=800,
                height=800,
                xaxis_title='',
                yaxis_title='%',
                template=metabolic_template,
                # name='My Legend Name'
                )

st.plotly_chart(fig, use_container_width=True)