

# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Custom Your Smoothie :cup_with_straw:")
st.write(
  """choose your prefered fruit for Smoothie"""
)

# Get the current credentials
cnx = st.connection('snowflake')
session = cnx.session()
#my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df =my_dataframe.to_pandas()



name_on_order = st.text_input('Name on Smoothie :')

st.write("Name will be  : ", name_on_order)    

ingredients_list=st.multiselect(
    "Choose up to 5 ingredients :",
    my_dataframe,
    max_selections = 5
)

btn_to_insert = st.button('Insert')

if ingredients_list : 
        ingredients_string=''
        for each_fruit in ingredients_list:
          ingredients_string += each_fruit + ' '
          search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
          st.write('The search value for ', each_fruit,' is ', search_on, '.')
         
          st.subheader(each_fruit+ ' Nutrition Information.')
          if search_on:
            smoothiefruit_res = requests.get("https://my.smoothiefroot.com/api/fruit/"+each_fruit)
            sf_df = st.dataframe(data=smoothiefruit_res.json(),use_container_width=True)
          else :
            st.write(" !!!! not found ")        

        st.write("Ingredients  : ", ingredients_string)    
    
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order +"""')"""

        #st.write(my_insert_stmt)
        if btn_to_insert :
            session.sql(my_insert_stmt).collect()
            st.success('Your smoothie is ordered', icon = '👍') 
      
   


