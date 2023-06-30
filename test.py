import time
import streamlit as st
import pandas as pd
column_config_dict = {

    "Geographical (decimal degrees)":{
        "Name": st.column_config.TextColumn(
            required=True, 
            default="P001", 
            max_chars=20, 
            validate=None),
         "Latitude": st.column_config.NumberColumn(
            required=True,
            #min_value=-31.00000000, 
            #max_value=-16.00000000,
            default=-22.00000000,
            format="%.8f",
            ),
        "Longitude": st.column_config.NumberColumn(
            required=True,
            #min_value=8.00000000, 
            #max_value=26.00000000,
            default=16.00000000,
            format="%.8f",
            ),
    },

    "Geographical (deg min sec)":{
        "Name": st.column_config.TextColumn(
            required=True,
            width="small",
            default="P001", 
            max_chars=20, 
            validate=None),
        "Lat_deg": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=-22,
            #min_value=-31, 
            #max_value=-16,
            format="%d",
            ),
        "Lat_min": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=0,
            min_value=0, 
            max_value=59,
            format="%d",
            ),
        "Lat_sec": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=0.00000,
            min_value=0.00000,
            max_value=59.99999,
            format="%.5f",
            ),
        "Lon_deg": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=16,
            #min_value=8,
            #max_value=26,
            format="%d",
            ),
        "Lon_min": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=0,
            min_value=0, 
            max_value=59,
            format="%d",
            ),
        "Lon_sec": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=0.00000,
            min_value=0.00000,
            max_value=59.99999,
            format="%.5f",
            ),
    },

    "Namibian (Gauss-Conform)":{
        "Name": st.column_config.TextColumn(
            required=True, 
            default="P001", 
            max_chars=20, 
            validate=None),
        "y": st.column_config.NumberColumn(
            required=True,
            format="%.3f",
            ),
        "x": st.column_config.NumberColumn(
            required=True,
            format="%.3f",
            ),
    },

    "UTM":{
        "Name": st.column_config.TextColumn(
            required=True, 
            default="P001", 
            max_chars=20, 
            validate=None),
        "y": st.column_config.NumberColumn(
            required=True,
            format="%.3f",
            ),
        "x": st.column_config.NumberColumn(
            required=True,
            format="%.3f",
            ),
    },
}


data = {"Name": "Brandberg", "Latitude": -21.14882548, "Longitude": 14.57821812}
input_df = pd.DataFrame(data, index=[0])
st.write(input_df)
source_df = input_df.copy()
if "newdf" not in st.session_state:
	st.session_state.newdf = pd.DataFrame()
if "editeddf" not in st.session_state:
	st.session_state.editeddf = pd.DataFrame()
if "temp_input_df" not in st.session_state:
	st.session_state.temp_input_df = input_df.copy()

def update():
	#st.write(st.session_state.data_editor)
	#st.write(st.session_state.data_editor["added_rows"])
	#st.write(st.session_state.data_editor["edited_rows"])
	st.session_state.newdf = pd.DataFrame(st.session_state.data_editor["added_rows"])
	st.session_state.editeddf = pd.DataFrame(st.session_state.data_editor["edited_rows"])
	
	
	#values = dict1.values()
	#for key, value in dict1.items():
	#	st.write(key, '->', value)
	#	st.write(type(key))
	#dict2 = st.session_state.data_editor["edited_rows"]	["0"]
	
	#st.write(type(list_of_dict["Latitude"]))

edited_df2 = st.data_editor(
                input_df,
                key="data_editor",
                num_rows="dynamic",
                hide_index=True,
                on_change=update,
                column_config=column_config_dict["Geographical (decimal degrees)"]
                )
added_rows_list = st.session_state.newdf.index.values.tolist()
edited_values_list = st.session_state.editeddf.index.values.tolist()
if not len(edited_values_list) == 0:
	for i in edited_values_list:
		st.session_state.temp_input_df.at[0,i] = st.session_state.editeddf.at[i,0]

input_df = pd.concat([st.session_state.temp_input_df, st.session_state.newdf], axis=0)

st.write(input_df)
#t.write(st.session_state.temp_input_df)

#st.write(st.session_state.editeddf)
#for i in edited_list:
#	source_df.at[0,i] = st.session_state.editeddf.at[i,0]
#st.write(source_df)

#vertical_concat = pd.concat([df1, df2], axis=0)
