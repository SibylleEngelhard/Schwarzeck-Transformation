import streamlit as st
from PIL import Image
import pandas as pd
import base64
from pyproj import transform, Transformer,CRS
import pydeck as pdk

#-----Page Configuration
st.set_page_config(page_title='Schwarzeck Transformation Namibia',
	page_icon='🌐',
	layout='wide',
	initial_sidebar_state='expanded')


#----menu button invisible
st.markdown(""" <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """, unsafe_allow_html=True)


#-----Projection Definition
Schwarzeck0=CRS.from_proj4("+proj=longlat +ellps=bess_nam +no_defs")
Schwarzeck1=CRS.from_proj4("+proj=longlat +ellps=bess_nam +towgs84=616.0,97.0,-251.0,0,0,0,0 +no_defs")
Schwarzeck2=CRS.from_proj4("+proj=longlat +ellps=bess_nam +towgs84=615.64,102.08,-255.81,0,0,0,0 +no_defs")
Schwarzeck3=CRS.from_proj4("+proj=longlat +ellps=bess_nam +towgs84=616.8,103.3,-256.9,0,0,0,0 +no_defs")
Lo11=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=11 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
Lo13=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=13 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
Lo15=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=15 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
Lo17=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=17 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
Lo18=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=18 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
Lo19=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=19 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
Lo21=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=21 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
Lo23=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=23 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
Lo25=CRS.from_proj4("+proj=tmerc +lat_0=-22 +lon_0=25 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs")
proj_dict={11:Lo11,13:Lo13,15:Lo15,17:Lo17,18:Lo18,19:Lo19,21:Lo21,23:Lo23,25:Lo25}
trafo_dict={'EPSG1226 Schwarzeck to WGS84(1)':Schwarzeck1,'EPSG1271 Schwarzeck to WGS84(2)':Schwarzeck2,'Default Schwarzeck to WGS84(3)':Schwarzeck3,'EPSG1226 WGS84 to Schwarzeck(1)':Schwarzeck1,'EPSG1271 WGS84 to Schwarzeck(2)':Schwarzeck2,'Default WGS84 to Schwarzeck(3)':Schwarzeck3}
utm_dict={'Zone 33S (15 E)':CRS(32733),'Zone 34S (21 E)':CRS(32734),'Zone 35S (27 E)':CRS(32735)}#trafo_Schw_WGS = TransformerGroup(CRS(4293),CRS(4326))
#trafo_WGS_Schw = TransformerGroup("epsg:4326","epsg:4293")
trafo_default_Schw_WGS = Transformer.from_crs(Schwarzeck3, CRS(4326),always_xy=True)
				
						

#----Image and Title 2 Columns
col1a, col1b= st.columns([5,1])
image = Image.open('trig2.jpg')

col1a.title('Schwarzeck - WGS84 Transformation Namibia')
col1b.image(image,width=180)

#App Description
col1a.markdown('''
This app converts and transforms between different coordinate systems in the Namibian Schwarzeck datum and WGS84 datum.
''')


#---------------------------------#
# About
expander_bar = st.expander('About this app')
expander_bar.markdown('''
- **Python libraries:** streamlit, pandas, pydeck, pyproj
- **Transformation Parameters:**  Default Transformation is *Schwarzeck to WGS84(3)*: DX=616.8 DY=103.3 DZ=-256.9 (X-Form, Dr. Charles Merry)   
Different transformations are selectable: *Schwarzeck to WGS84(1)* https://epsg.io/1226 or *Schwarzeck to WGS84(2)* https://epsg.io/1271
- No warranty is given that the information provided in this app is free of errors - your use of this app and your reliance on any information on it is solely at your own risk.
- **written by:** Sibylle Engelhard - African Geomatics  https://www.africangeomatics.com
''')

#---------------------------------#

#Function to download dataframes as csv
def filedownload(df,download_name,showtext):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download='+download_name+'>'+showtext+'</a>'
    return href

#Configure sidebar
st.sidebar.subheader("View Input Coordinates on Map:")
	
col2a,col2b,col2c= st.columns([5,2,3])

with col2a:
	map_df = pd.read_csv('dec.csv')
	map_df['latitude']=map_df['Latitude']
	map_df['longitude']=map_df['Longitude']
	st.write(map_df)
	#Calculate wgs coords and display on map
	
	
	##temp = map_df[["Name","latitude", "longitude"]]
	#st.write(df)

	st.map(map_df)

	