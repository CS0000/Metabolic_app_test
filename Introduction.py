st.set_page_config(layout="wide")

from helper import *



# tabs_font_css = """
# <style>
# button[data-baseweb="tab"] {
#   font-size: 35px;
# }
# </style>
# """
# st.write(tabs_font_css, unsafe_allow_html=True)

st.header('test page')


annotated_text(('commoditiy1','group1','#d5de81'))
annotated_text(('commoditiy2','group1','#fccb7d'))
annotated_text(('commoditiy3','group2','#2eaf62'))
annotated_text(annotation('commoditiy4','group3','#d64973',font_size='40px'))

