from helper import *


st.header('Welcom to Interactive Visualization Tool (demo)')
st.subheader("from Agrifood & Biodiversity team")
st.write("This interative visualization tool is designed to self-service exploratory data analysis, allowing consultants and clients to explore the sustainability data under different angles and levels of aggregations, supporting the implementation of SBTN framework.")

st.image('./data/intro.png',caption="demonstration of 3 functional pages")
st.info("""
**Preliminary exploration page**:         
        - Have a general overview of the environmental impacts in single commodity categories.             
        - Break down certain categories and see detailed contributions of the environmental impact within this category. 
        
**Bar view page**:        
        - visualize pressure dataset to be bar charts, flexible to customize and filtering the datasets in a tree-structured manner.            

**Map view page**:            
        - combining pressure contribution and SoN mapping
        - exploration on global and local scale              
""")
# annotated_text(('commoditiy1','group1','#d5de81'))
# annotated_text(('commoditiy2','group1','#fccb7d'))
# annotated_text(('commoditiy3','group2','#2eaf62'))
# annotated_text(annotation('commoditiy4','group3','#d64973',font_size='40px'))

procede = False

if 'df' not in st.session_state:
    C1,C2,submitted = df_input_form()

    if (len(C1)!=0)&(len(C2)!=0):
        procede = True
        st.info("Submitted!")
    else:
        procede = False 

    if procede == True:
        try:
                SHEET_CODE, WORK_SHEET_NAME = C1,C2
                st.write(f"unique sheet code: {SHEET_CODE}, work sheet name: {WORK_SHEET_NAME}")
                conn1 = st.connection(SHEET_CODE,type=GSheetsConnection)
                pressure = conn1.read(worksheet=WORK_SHEET_NAME)

                st.session_state.df = pressure
                with st.expander('Preview dataset'):
                        st.dataframe(pressure.head())
        except ValueError:
                st.error('Please enter a valid input')
else:
      st.warning("""You've already locate to a dataset, see preview of the dataset below. Refresh the page if you want to locate to another dataset.""")
      st.dataframe(st.session_state.df.head())
              




