# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


session = get_active_session()


my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.ORDERS")
           .select("NAME_ON_ORDER", "INGREDIENTS", "ORDER_FILLED")
           .filter(col("ORDER_FILLED") == False)   # only show unfilled orders
           .to_pandas()
)

editable_df = st.data_editor(
    my_dataframe,
    use_container_width=True,
    hide_index=True
)



submitted = st.button('Submit')

if submitted:
    st.success("Someone clicked the button.", icon='👍')
