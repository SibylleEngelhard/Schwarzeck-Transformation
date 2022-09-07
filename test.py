import streamlit as st

import pandas as pd
import pydeck as pdk

#-----Page Configuration
st.set_page_config(page_title='Test',
	page_icon='🌐',
	layout='wide')

st.title('Test')

example_listofdicts = [
	{'Name': 'A', 'lat':-22.57492041, 'lon':17.08943187},
	{'Name': 'B', 'lat':-19.54495314, 'lon':18.07635639},
	{'Name': 'C', 'lat':-19.95534285, 'lon':14.00000144},
	{'Name': 'D', 'lat':-27.9735897, 'lon':16.74977476},
	{'Name': 'E', 'lat':-18.0421342, 'lon':21.99427305},
	{'Name': 'F', 'lat':-24.48714568, 'lon':15.79964004},
	{'Name': 'G', 'lat':-26.72039216, 'lon':17.99995017}]

df1 = pd.DataFrame(example_listofdicts)
st.write(df1.style.format({'lat': '{:,.8f}', 'lon': '{:,.8f}'}))

col1, col2, col3 = st.columns(3,gap='large')

with col1:
	st.map(df1)

with col2:
	st.pydeck_chart(pdk.Deck(
			map_style='mapbox://styles/mapbox/outdoors-v11',
			initial_view_state=pdk.ViewState(
			latitude=-23,
			longitude=18,
			zoom=4),
			layers=[pdk.Layer(
					'ScatterplotLayer',
					data=df1,
					get_position=['lon', 'lat'],
					get_color='[200, 30, 0, 160]',
					radius_min_pixels=4,
	    			radius_max_pixels=15,
					)
				]
		))
with col3:
	st.pydeck_chart(pdk.Deck(
			map_style='mapbox://styles/mapbox/satellite-streets-v11',
			initial_view_state=pdk.ViewState(
			latitude=-23,
			longitude=18,
			zoom=4),
			layers=[pdk.Layer(
					'ScatterplotLayer',
					data=df1,
					get_position=['lon', 'lat'],
					get_color='[200, 30, 0, 160]',
					radius_min_pixels=4,
	    			radius_max_pixels=15,
					)
				]
		))

