import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

# snowpark session creation here (get_session()), then:
sp_df = (session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
               .select(col("FRUIT_NAME"), col("SEARCH_ON"))
               .sort(col("FRUIT_NAME")))

# Pandas copy for easy lookup
pd_df = sp_df.to_pandas()


st.subheader("Build your smoothie")

fruit_choices = pd_df["FRUIT_NAME"].tolist()
ingredients_list = st.multiselect("Choose fruits:", fruit_choices)

# Lookup SEARCH_ON value for each selected fruit
def to_search_term(fruit_label: str) -> str:
    row = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_label, "SEARCH_ON"]
    return row.iloc[0] if not row.empty else fruit_label  # fallback

search_terms = [to_search_term(f) for f in ingredients_list]

# Show the mapping to the user (handy while testing)
if ingredients_list:
    st.write("Search terms:", search_terms)


if ingredients_list:
    fruit_chosen = ingredients_list[0]
    search_on = to_search_term(fruit_chosen)
    st.write(f"The search value for {fruit_chosen} is {search_on}.")

    try:
        resp = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}",
            timeout=10
        )
        if resp.ok:
            data = resp.json()
            # normalize to list for consistent display
            if isinstance(data, dict):
                data = [data]
            st.json(data)
            st.dataframe(pd.json_normalize(data), use_container_width=True)
        else:
            st.warning(f"No data found for '{search_on}' (HTTP {resp.status_code}).")
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
