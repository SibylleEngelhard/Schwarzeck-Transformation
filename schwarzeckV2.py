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
	st.header('Source System')
	source_datum=st.radio ('Source Datum',('Schwarzeck','WGS84'),key='testa')
	st.write(' ')
	st.write(' ')
	st.write(' ')
	st.write(' ')
	
with col2b:
	st.header('Target System')
	target_datum=st.radio ('Target Datum',('Schwarzeck','WGS84'),key="testb")

with col2c:
	if source_datum != target_datum:
		trafo_description_dict={'EPSG1226 Schwarzeck to WGS84(1)':'DX=616.0  DY=97.0  DZ=-251.0','EPSG1271 Schwarzeck to WGS84(2)':'DX=615.64  DY=102.08  DZ=-255.81','Default Schwarzeck to WGS84(3)':'DX=616.8  DY=103.3  DZ=-256.9','EPSG1226 WGS84 to Schwarzeck(1)':'DX=-616.0  DY=-97.0  DZ=251.0','EPSG1271 WGS84 to Schwarzeck(2)':'DX=-615.64  DY=-102.08  DZ=255.81','Default WGS84 to Schwarzeck(3)':'DX=-616.8  DY=-103.3  DZ=256.9'}
		
		if source_datum=='Schwarzeck':
			datum_transformation=st.selectbox('Datum Transformation',['EPSG1226 Schwarzeck to WGS84(1)','EPSG1271 Schwarzeck to WGS84(2)','Default Schwarzeck to WGS84(3)'],index=2)
		else:
			datum_transformation=st.selectbox('Datum Transformation',['EPSG1226 WGS84 to Schwarzeck(1)','EPSG1271 WGS84 to Schwarzeck(2)','Default WGS84 to Schwarzeck(3)'],index=2)
		
		text_trafo_description=trafo_description_dict[datum_transformation]
		st.markdown("<small style='color: #f63366'>Transformation Parameters: <br>"+text_trafo_description+"</small>", unsafe_allow_html=True) 
	

		trafo_Schw_WGS = Transformer.from_crs(trafo_dict[datum_transformation], CRS(4326),always_xy=True)
		trafo_WGS_Schw = Transformer.from_crs(CRS(4326),trafo_dict[datum_transformation],always_xy=True)
		

col3a, col3b,col3c,col3d= st.columns([3,2,3,2])

with col3a:	
	if source_datum=='Schwarzeck':
		source_coord_syst = st.radio('Source Coordinate System',('Geographical (decimal degrees)','Geographical (deg min sec)','Namibian (Gauss-Conform)'))
	else:
		source_coord_syst = st.radio('Source Coordinate System',('Geographical (decimal degrees)','Geographical (deg min sec)','UTM'))
	
	
with col3b:
	if source_coord_syst == 'Namibian (Gauss-Conform)':
		st.subheader(' ')
		source_central_meridian = st.selectbox('Source Projection Central Meridian',[11,13,15,17,18,19,21,23,25],index=3)
		source_CRS=proj_dict[source_central_meridian]
	if source_coord_syst == 'UTM':
		st.subheader(' ')
		source_utm_zone = st.selectbox('Source UTM Zone',['Zone 33S (15 E)','Zone 34S (21 E)','Zone 35S (27 E)'],index=0)
		source_CRS=utm_dict[source_utm_zone]
with col3c:
	if target_datum=='Schwarzeck':
		target_coord_syst = st.radio('Target Coordinate System',('Geographical (decimal degrees)','Geographical (deg min sec)','Namibian (Gauss-Conform)'),key="target_schwarzeck")
	else:
		target_coord_syst = st.radio('Target Coordinate System',('Geographical (decimal degrees)','Geographical (deg min sec)','UTM'),key="target_wgs")
	
with col3d:	
	if target_coord_syst == 'Namibian (Gauss-Conform)':
		st.subheader(' ')
		target_central_meridian = st.selectbox('Target Projection Central Meridian',[11,13,15,17,18,19,21,23,25],index=3)
		target_CRS=proj_dict[target_central_meridian]
	
	if target_coord_syst == 'UTM':
		st.subheader(' ')
		target_utm_zone = st.selectbox('Target UTM Zone',['Zone 33S (15 E)','Zone 34S (21 E)','Zone 35S (27 E)'],index=0)
		target_CRS=utm_dict[target_utm_zone]

col4a, col4b= st.columns(2)
		
with col4a:
	#choose input method
	expander2 = st.expander('Click to choose your input method')
	input_method = expander2.radio('',('CSV File','Coordinate Input'))
	
	#CSV File
	if input_method=='CSV File':
		#Creating example Dataframes from csv files
		if source_datum=='Schwarzeck' :
			if 	source_coord_syst == 'Geographical (deg min sec)':
				example_df = pd.read_csv('dms.csv')
				example_name='degminsec.csv'
				example_text='Download Example CSV File - Geographical (deg min sec)'
			elif source_coord_syst == 'Geographical (decimal degrees)':
				example_df = pd.read_csv('dec.csv')
				example_name='decimaldeg.csv'
				example_text='Download Example CSV File - Geographical (decimal degrees)'
			else:
				example_df = pd.read_csv('Lo22'+str(source_central_meridian)+'.csv')
				example_name='Lo22'+str(source_central_meridian)+'.csv'
				example_text='Download Example CSV File - Namibian (Gauss-Conform)'
		else:
			if 	source_coord_syst == 'Geographical (deg min sec)':
				example_df = pd.read_csv('wgsdms.csv')
				example_name='degminsec.csv'
				example_text='Download Example CSV File - Geographical (deg min sec)'
			elif source_coord_syst == 'Geographical (decimal degrees)':
				example_df = pd.read_csv('wgsdec.csv')
				example_name='decimaldeg.csv'
				example_text='Download Example CSV File - Geographical (decimal degrees)'
			else:
				utm_zone=source_utm_zone[5:7]
				example_df = pd.read_csv('utm'+utm_zone+'.csv')
				example_name='utm'+utm_zone+'.csv'
				example_text='Download Example CSV File - UTM'
		
		# Download link for csv file according to coordinate system
		# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
		expander2.markdown(filedownload(example_df,example_name,example_text), unsafe_allow_html=True)
		
		#Upload File
		file_check=False
		NaN_values=False
		uploaded_file = expander2.file_uploader('Upload your input CSV file', type=['csv'])	

		if uploaded_file is not None:

			try:
				input_df = pd.read_csv(uploaded_file)
			except:
				try:
					input_df = pd.read_csv(uploaded_file,encoding='latin-1')
				except:
					st.warning("Error with file encoding. Please delete special characters (ä.ö,ü,...). Or try opening and saving the file in a text editor with encoding 'utf-8'.")
		
			if input_df.isnull().values.any():
				st.warning("File contains rows with empty values, these rows were not transformed")
				NaN_values=True

			if source_coord_syst == 'Namibian (Gauss-Conform)':
				try:	
					select=input_df[['Name','y','x']]
					file_check=True
					source_df=input_df.copy()
				except:
					st.warning("Uploaded file must include the columns: Name, y, x")
					input_df = example_df
					source_df=input_df.copy()
			elif source_coord_syst == 'Geographical (deg min sec)':
				try:	
					select=input_df[['Name','Lat_deg','Lat_min','Lat_sec','Lon_deg','Lon_min','Lon_sec']]
					file_check=True
					source_df=input_df.copy()
				except:
					st.warning("Uploaded file must include the columns: Name, Lat_deg, Lat_min, Lat_sec, Lon_deg, Lon_min, Lon_sec")
					input_df = example_df
					source_df=input_df.copy()	
			elif source_coord_syst == 'Geographical (decimal degrees)':
				try:	
					select=input_df[['Name','Latitude','Longitude']]
					file_check=True
					source_df=input_df.copy()
				except:
					st.warning("Uploaded file must include the columns: Name, Latitude, Longitude")
					input_df = example_df
					source_df=input_df.copy()
			else:
				try:	
					select=input_df[['Name','East','North']]
					file_check=True
					source_df=input_df.copy()
				except:
					st.warning("Uploaded file must include the columns: Name, East, North")
					input_df = example_df
					source_df=input_df.copy()	

			if NaN_values:
				#input_df.dropna()
				source_df=source_df.dropna()	
		else:
			input_df = example_df
			source_df=input_df.copy()
			



	
	#Coordinate Input
	else:
		if source_datum=='Schwarzeck' :
			
			if 	source_coord_syst == 'Namibian (Gauss-Conform)':
				lo_df = pd.read_csv('lo_dict.csv',index_col=0)
				lo_dict=lo_df.to_dict('index')
				selected_coord=lo_dict[source_central_meridian]
				
				def user_input_yx(coord_dict):
					name = expander2.text_input('Name', coord_dict['Name'])
					y = expander2.number_input('y (East)',value=coord_dict['y'],format='%.3f')
					x = expander2.number_input('x (North)',value=coord_dict['x'],format='%.3f')
					data = {'Name': name,
				        'y': y,
				        'x': x}
					user_input = pd.DataFrame(data, index=[0])
					return user_input
				
				input_df = user_input_yx(selected_coord)

				
			elif source_coord_syst == 'Geographical (deg min sec)':
				
				def user_input_dms():
					name = expander2.text_input('Name', 'Brandberg')
					lat_deg = expander2.number_input('Lat deg',value=-21,min_value=-31,max_value=-16)
					lat_min = expander2.number_input('Lat min',value=8,min_value=0,max_value=59)
					lat_sec= expander2.number_input('Lat sec',value=55.78348,min_value=0.00000,max_value=59.99999,format='%.5f')
					lon_deg = expander2.number_input('Lon deg',value=14,min_value=8,max_value=26)
					lon_min = expander2.number_input('Lon min',value=34,min_value=0,max_value=59)
					lon_sec= expander2.number_input('Lon sec',value=41.59803,min_value=0.00000,max_value=59.99999,format='%.5f')
					data = {'Name': name,
				        'Lat_deg': lat_deg,
				        'Lat_min': lat_min,
				        'Lat_sec': lat_sec,
				        'Lon_deg': lon_deg,
				        'Lon_min': lon_min,
				        'Lon_sec': lon_sec}
					user_input = pd.DataFrame(data, index=[0])
					return user_input
				
				input_df = user_input_dms()
			else: 

				def user_input_dec():
					name = expander2.text_input('Name', 'Brandberg')
					lat = expander2.number_input('Latitude',value=-21.14882548,min_value=-31.00000000,max_value=-16.00000000,format='%.8f')
					lon = expander2.number_input('Longitude',value=14.57821812,min_value=8.00000000,max_value=26.00000000,format='%.8f')
					data = {'Name': name,
				        'Latitude': lat,
				        'Longitude': lon}
					user_input = pd.DataFrame(data, index=[0])
					return user_input
				
				input_df = user_input_dec()
		else:
			if 	source_coord_syst == 'Geographical (deg min sec)':
				
				def user_input_wgsdms():
					name = expander2.text_input('Name', 'T008')
					lat_deg = expander2.number_input('Lat deg',value=-21,min_value=-31,max_value=-16)
					lat_min = expander2.number_input('Lat min',value=8,min_value=0,max_value=59)
					lat_sec= expander2.number_input('Lat sec',value=57.69950,min_value=0.00000,max_value=59.99999,format='%.5f')
					lon_deg = expander2.number_input('Lon deg',value=14,min_value=8,max_value=26)
					lon_min = expander2.number_input('Lon min',value=34,min_value=0,max_value=59)
					lon_sec= expander2.number_input('Lon sec',value=39.66941,min_value=0.00000,max_value=59.99999,format='%.5f')
					data = {'Name': name,
				        'Lat_deg': lat_deg,
				        'Lat_min': lat_min,
				        'Lat_sec': lat_sec,
				        'Lon_deg': lon_deg,
				        'Lon_min': lon_min,
				        'Lon_sec': lon_sec}
					user_input = pd.DataFrame(data, index=[0])
					return user_input
				
				input_df = user_input_wgsdms()
			elif source_coord_syst == 'Geographical (decimal degrees)':
				
				def user_input_wgsdec():
					name = expander2.text_input('Name', 'T008')
					lat = expander2.number_input('Latitude',value=-21.14936097,min_value=-31.00000000,max_value=-16.00000000,format='%.8f')
					lon = expander2.number_input('Longitude',value=14.57768595,min_value=8.00000000,max_value=26.00000000,format='%.8f')
					data = {'Name': name,
				        'Latitude': lat,
				        'Longitude': lon}
					user_input = pd.DataFrame(data, index=[0])
					return user_input
				
				input_df = user_input_wgsdec()
			else:
				utm_df = pd.read_csv('utm_coord_dict.csv',index_col=0)
				utm_coord_dict=utm_df.to_dict('index')
				selected_coord=utm_coord_dict[int(source_utm_zone[5:7])]
				
				def user_input_utm(coord_dict):
					name = expander2.text_input('Name', coord_dict['Name'])
					east = expander2.number_input('East',value=coord_dict['East'],format='%.3f')
					north = expander2.number_input('North',value=coord_dict['North'],format='%.3f')
					data = {'Name': name,
				        'East': east,
				        'North': north}
					user_input = pd.DataFrame(data, index=[0])
					return user_input
				
				input_df = user_input_utm(selected_coord)
		#definition of source_df after coordinate input
		source_df=input_df.copy()
		file_check=True
	
	#Source System
	if source_coord_syst == 'Namibian (Gauss-Conform)':
		source_coord_syst_text='Lo22/'+str(source_central_meridian)
	elif source_coord_syst == 'Geographical (deg min sec)':
		source_coord_syst_text='- deg min sec'	
	elif source_coord_syst == 'Geographical (decimal degrees)':
		source_coord_syst_text='- decimal degrees'
	else:
		source_coord_syst_text='UTM '+source_utm_zone[:-7]


	st.subheader('Source Coordinates')	
		#Info about input received
	if input_method=='CSV File':
		if uploaded_file is not None and file_check==True:
			st.write('Uploaded file ('+source_datum+' '+source_coord_syst_text+'): '+uploaded_file.name)
		else:
			st.write('Awaiting CSV file to be uploaded. Currently using example coordinates:')
	else:	
		st.write(source_datum+' '+source_coord_syst_text)
		
			
	
	
	#Display input_df and calculate lat long for source_df		
	if source_coord_syst == 'Namibian (Gauss-Conform)':
		

		st.write(input_df.style.format({'y': '{:,.3f}', 'x': '{:,.3f}'}))
		

		trafo_yx_Schw = Transformer.from_crs(source_CRS, Schwarzeck0,always_xy=True)
		lon,lat=trafo_yx_Schw.transform(source_df['y'],source_df['x'])
		
		source_df['Latitude']=lat
		source_df['Longitude']=lon
		del source_df['y']
		del source_df['x']
		

	elif source_coord_syst == 'Geographical (deg min sec)':
		
		st.write(input_df.style.format({'Lat_deg':'{:,.0f}','Lat_min':'{:,.0f}','Lat_sec': '{:,.5f}', 'Lon_deg':'{:,.0f}','Lon_min':'{:,.0f}','Lon_sec': '{:,.5f}'}))
		
		source_df['Latitude']=source_df['Lat_deg']-source_df['Lat_min']/60-source_df['Lat_sec']/3600
		source_df['Longitude']=source_df['Lon_deg']+source_df['Lon_min']/60+source_df['Lon_sec']/3600
		del source_df['Lat_deg']
		del source_df['Lat_min']
		del source_df['Lat_sec']
		del source_df['Lon_deg']
		del source_df['Lon_min']
		del source_df['Lon_sec']
	
	elif source_coord_syst == 'Geographical (decimal degrees)':
		
		st.write(input_df.style.format({'Latitude': '{:,.8f}', 'Longitude': '{:,.8f}'}))
	
	else:
		st.write(input_df.style.format({'East': '{:,.3f}', 'North': '{:,.3f}'}))
		trafo_utm_wgs = Transformer.from_crs(source_CRS, CRS(4326),always_xy=True)

		lonw,latw=trafo_utm_wgs.transform(source_df['East'],source_df['North'])
		
		source_df['Latitude']=latw
		source_df['Longitude']=lonw
		del source_df['East']
		del source_df['North']

	
	#Calculate wgs coords and display on map
	map_df=source_df.copy()	
	if source_datum=='Schwarzeck':
		wgs_lon,wgs_lat=trafo_default_Schw_WGS.transform(source_df['Longitude'],source_df['Latitude'])
		map_df['latitude']=wgs_lat
		map_df['longitude']=wgs_lon

	else:
		map_df['latitude']=map_df['Latitude']
		map_df['longitude']=map_df['Longitude']
	
	temp = map_df[["latitude", "longitude"]]

	#to_map_image=True
	placeholder_button=st.sidebar.empty()
	placeholder_map=st.sidebar.empty()
	button1=placeholder_button.button('Show Satellite Image',key='initial_state')
	button2=False
	placeholder_map.pydeck_chart(pdk.Deck(
			map_style='mapbox://styles/mapbox/outdoors-v11',
			initial_view_state=pdk.ViewState(
			latitude=-23,
			longitude=18,
			zoom=4),
			layers=[pdk.Layer(
					'ScatterplotLayer',
					data=map_df,
					get_position=['longitude', 'latitude'],
					get_color='[200, 30, 0, 160]',
					radius_min_pixels=4,
	    			radius_max_pixels=15,
					)
				]
		))


	if button1:
		placeholder_button.empty()
		button2=placeholder_button.button('Show Map Image',key='initial_state2')
		placeholder_map.empty()
		placeholder_map.pydeck_chart(pdk.Deck(
		map_style='mapbox://styles/mapbox/satellite-streets-v11',
		initial_view_state=pdk.ViewState(
		latitude=-23,
		longitude=18,
		zoom=4),
		layers=[pdk.Layer(
				'ScatterplotLayer',
				data=map_df,
				get_position=['longitude', 'latitude'],
				get_color='[0, 0, 255,160]',
				radius_min_pixels=4,
    			radius_max_pixels=15,
				)
			]
		))
		
	if button2:
		placeholder_button.empty()
		button1=placeholder_button.button('Show Satellite Image',key='initial_state')
		placeholder_map.empty()
		placeholder_map.pydeck_chart(pdk.Deck(
			map_style='mapbox://styles/mapbox/outdoors-v11',
			initial_view_state=pdk.ViewState(
			latitude=-23,
			longitude=18,
			zoom=4),
			layers=[pdk.Layer(
					'ScatterplotLayer',
					data=map_df,
					get_position=['longitude', 'latitude'],
					get_color='[200, 30, 0, 160]',
					radius_min_pixels=4,
	    			radius_max_pixels=15,
					)
				]
		))
	

#Target System
with col4b:
	
	placeholder_inputmethod=st.empty()
	placeholder_inputmethod.header(' ')
	target_df=source_df.copy()
	if target_coord_syst == 'Namibian (Gauss-Conform)':
		target_coord_syst_text='Lo22/'+str(target_central_meridian)
	elif target_coord_syst == 'Geographical (deg min sec)':
		target_coord_syst_text='- deg min sec'	
	elif target_coord_syst == 'Geographical (decimal degrees)':
		target_coord_syst_text='- decimal degrees'
	else:
		target_coord_syst_text='UTM '+target_utm_zone[:-7]


	st.subheader('Target Coordinates')
	if not file_check ==True:
		st.write('Awaiting CSV file to be uploaded. Currently using example coordinates:')
	else:	
		st.write(target_datum+' '+target_coord_syst_text)

	
	#Datum Transformation 
	if source_datum== 'Schwarzeck' and target_datum=='WGS84':
		wgs_lon,wgs_lat=trafo_Schw_WGS.transform(source_df['Longitude'],source_df['Latitude'])
		target_df['Latitude']=wgs_lat
		target_df['Longitude']=wgs_lon
		
	elif source_datum== 'WGS84' and target_datum=='Schwarzeck':
		schw_lon,schw_lat=trafo_WGS_Schw.transform(source_df['Longitude'],source_df['Latitude'])
		target_df['Latitude']=schw_lat
		target_df['Longitude']=schw_lon
		
	
	#edit target dataframe
	if target_coord_syst == 'Namibian (Gauss-Conform)':
		
		trafo_Schw_Lo = Transformer.from_crs(Schwarzeck0,target_CRS,always_xy=True)
		y,x=trafo_Schw_Lo.transform(target_df['Longitude'],target_df['Latitude'])
		target_df['x']=x
		target_df['y']=y
		del target_df['Latitude']
		del target_df['Longitude']		
		
		target_df=target_df[['Name','y','x']]
		target_df=target_df.round(3)
		st.write(target_df.style.format({'y': '{:,.3f}', 'x': '{:,.3f}'}))
		
	
	elif target_coord_syst == 'Geographical (deg min sec)':
		
		target_df['Lat_deg']=target_df['Latitude'].astype(int)
		target_df['Lat_min_dec']=(target_df['Lat_deg']-target_df['Latitude'])*60
		target_df['Lat_min']=target_df['Lat_min_dec'].astype(int)     
		target_df['Lat_sec']=(target_df['Lat_min_dec']-target_df['Lat_min'])*60
		target_df['Lon_deg']=target_df['Longitude'].astype(int)
		target_df['Lon_min_dec']=(target_df['Longitude']-target_df['Lon_deg'])*60
		target_df['Lon_min']=target_df['Lon_min_dec'].astype(int)       
		target_df['Lon_sec']=(target_df['Lon_min_dec']-target_df['Lon_min'])*60
		del target_df['Lat_min_dec']
		del target_df['Lon_min_dec']
		del target_df['Latitude']
		del target_df['Longitude']
		
		target_df=target_df[['Name','Lat_deg','Lat_min','Lat_sec','Lon_deg','Lon_min','Lon_sec']]
		target_df=target_df.round(5)
		st.write(target_df.style.format({'Lat_sec': '{:,.5f}', 'Lon_sec': '{:,.5f}'}))
		
	elif target_coord_syst == 'Geographical (decimal degrees)':
		
		target_df=target_df[['Name','Latitude','Longitude']]
		target_df=target_df.round(8)
		st.write(target_df.style.format({'Latitude': '{:,.8f}', 'Longitude': '{:,.8f}'}))
	
	else:
		trafo_wgs_utm = Transformer.from_crs(CRS(4326),target_CRS,always_xy=True)
		east,north=trafo_wgs_utm.transform(target_df['Longitude'],target_df['Latitude'])
		target_df['East']=east
		target_df['North']=north
		del target_df['Latitude']
		del target_df['Longitude']		
		
		target_df=target_df[['Name','East','North']]
		target_df=target_df.round(3)
		st.write(target_df.style.format({'East': '{:,.3f}', 'North': '{:,.3f}'}))
		
	#define file download name
	if target_coord_syst == 'Namibian (Gauss-Conform)':
		output_name='Lo22'+str(target_central_meridian)+'.csv'
		output_text='Download Output File - Namibian (Gauss-Conform)'
	elif target_coord_syst == 'Geographical (deg min sec)':
		output_name='degminsec.csv'
		output_text='Download Output File - Geographical (deg min sec)'
	elif target_coord_syst == 'Geographical (decimal degrees)':
		output_name='decimaldeg.csv'
		output_text='Download Output File - Geographical (decimal degrees)'
	else:
		output_name='utm'+target_utm_zone[5:7]+'.csv'
		output_text='Download Output File - UTM'
	
	#target file download
	st.markdown(filedownload(target_df,output_name,output_text), unsafe_allow_html=True)

