import base64
import streamlit as st
from PIL import Image
import pandas as pd
from pyproj import transform, Transformer, CRS
import pydeck as pdk


def change_map_view():
    st.session_state.map_view = not st.session_state.map_view

@st.cache_data
def example_source_upload(filename):
    # uploads example source csv file and returns dataframe
    df = pd.read_csv(filename)
    return df

@st.cache_data
def create_example_coords_dict():
    # creates dictionary with one example coordinate for each selectable coordinate system
    example_coords_dict = {
        "Schwarzeck":{
            "Geographical (decimal degrees)":{
                0:{
                    "Name": "Brandberg",
                    "Latitude": -21.14882548,
                    "Longitude": 14.57821812,
                },
             },             
            "Geographical (deg min sec)": {
                0:{
                    "Name": "Brandberg",
                    "Lat_deg": -21,
                    "Lat_min": 8,
                    "Lat_sec": 55.78348,
                    "Lon_deg": 14, 
                    "Lon_min": 34, 
                    "Lon_sec": 41.59803,
                },
            },
            "Namibian (Gauss-Conform)":{
                11: {
                    "Name": "Kunene",
                    "y": -81059.409,
                    "x": -523748.244,
                },
                13: {
                    "Name": "Victor",
                    "y": -23030.1,
                    "x": -386483.6,
                },
                15: {
                    "Name": "Brandberg",
                    "y": 43804,
                    "x": -94178,
                },
                17: {
                    "Name": "Omatako",
                    "y": 29823.33,
                    "x": -88258.09,
                },
                18: {
                    "Name": "Schlangenkopf",
                    "y": 13136.25,
                    "x": 524801.378,
                },
                19: {
                    "Name": "Schwarzeck",
                    "y": 33244.91,
                    "x": 84181.32,
                },
                21: {
                    "Name": "Gam",
                    "y": 18455.47,
                    "x": -193858.67,
                },
                23: {
                    "Name": "KB1",
                    "y": -17030.32,
                    "x": -463724.954,
                },
                25: {
                    "Name": "KATM",
                    "y": 71880.011,
                    "x": -497662.898,
                },
            },
        },
        "WGS84":{
            "Geographical (decimal degrees)":{
              0:{ #wgs
                    "Name": "T008",
                    "Latitude": -21.14936097,
                    "Longitude": 14.57768595,
                },
            },           
            "Geographical (deg min sec)": {
                0:{#wgs
                    "Name": "T008",
                    "Lat_deg": -21,
                    "Lat_min": 8,
                    "Lat_sec": 57.69950,
                    "Lon_deg": 14, 
                    "Lon_min": 34, 
                    "Lon_sec": 39.66941,
                },
            },
            "UTM":{
                "Zone 33S (15 E)": {
                    "Name": "SESR",
                    "East": 581024.898,
                    "North": 7291603.569,
                },
                "Zone 34S (21 E)": {
                    "Name": "MUHO",
                    "East": 392751.159,
                    "North": 8019425.879,
                },
                "Zone 35S (27 E)": {
                    "Name": "KATM",
                    "East": 215587.278,
                    "North": 8062712.461,
                },
            },
        },    
    }
    return example_coords_dict

@st.cache_data
def create_example_df(source_datum,source_coord_system,source_proj_id=0):
    # creates dataframe with one example coordinate with selected coord system settings from cached dictionary
    example_coords_dict=create_example_coords_dict()
    return pd.DataFrame(example_coords_dict[source_datum][source_coord_system][source_proj_id], index=[0])

@st.cache_data
def load_image():
    st.image("trig2.jpg",width=180)
    
# Function to download dataframes as csv
def filedownload(df, download_name, showtext):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = (
        f'<a href="data:file/csv;base64,{b64}" download='
        + download_name
        + ">"
        + showtext
        + "</a>"
    )
    return href

def reset_dataeditor_dfs():
    st.session_state.newdf = pd.DataFrame()
    st.session_state.editeddf = pd.DataFrame()

def update_editable_dataframe():
    st.session_state.newdf = pd.DataFrame(st.session_state.data_editor["added_rows"])
    st.session_state.editeddf = pd.DataFrame(st.session_state.data_editor["edited_rows"])
 
          

# --------------------------------- #

# ---- Page Configuration ---- #
st.set_page_config(
    page_title="Schwarzeck Transformation Namibia",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "input_method" not in st.session_state:
    st.session_state.input_method = "Upload CSV File"


# ---- menu button invisible ---- #
st.markdown(
    """ <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """,
    unsafe_allow_html=True,
)


# ---- Projection Definitions and Settings ---- #
Schwarzeck0 = CRS.from_proj4("+proj=longlat +ellps=bess_nam +no_defs")
Schwarzeck1 = CRS.from_proj4(
    "+proj=longlat +ellps=bess_nam +towgs84=616.0,97.0,-251.0,0,0,0,0 +no_defs"
)
Schwarzeck2 = CRS.from_proj4(
    "+proj=longlat +ellps=bess_nam +towgs84=615.64,102.08,-255.81,0,0,0,0 +no_defs"
)
Schwarzeck3 = CRS.from_proj4(
    "+proj=longlat +ellps=bess_nam +towgs84=616.8,103.3,-256.9,0,0,0,0 +no_defs"
)

proj_dict = {
    11: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=11 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
    13: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=13 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
    15: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=15 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
    17: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=17 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
    18: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=18 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
    19: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=19 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
    21: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=21 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
    23: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=23 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
    25: CRS.from_proj4(
    "+proj=tmerc +lat_0=-22 +lon_0=25 +k=1 +x_0=0 +y_0=0 +axis=wsu +ellps=bess_nam +to_meter=1.0000135965 +no_defs"
    ),
}
trafo_dict = {
    "EPSG1226 Schwarzeck to WGS84(1)": Schwarzeck1,
    "EPSG1271 Schwarzeck to WGS84(2)": Schwarzeck2,
    "Default Schwarzeck to WGS84(3)": Schwarzeck3,
    "EPSG1226 WGS84 to Schwarzeck(1)": Schwarzeck1,
    "EPSG1271 WGS84 to Schwarzeck(2)": Schwarzeck2,
    "Default WGS84 to Schwarzeck(3)": Schwarzeck3,
}
utm_dict = {
    "Zone 33S (15 E)": CRS(32733),
    "Zone 34S (21 E)": CRS(32734),
    "Zone 35S (27 E)": CRS(32735),
}  


trafo_default_Schw_WGS = Transformer.from_crs(Schwarzeck3, CRS(4326), always_xy=True)

if "map_view" not in st.session_state:
    st.session_state.map_view = True

if "newdf" not in st.session_state:
    st.session_state.newdf = pd.DataFrame()
if "editeddf" not in st.session_state:
    st.session_state.editeddf = pd.DataFrame()
#if "temp_input_df" not in st.session_state:
#    st.session_state.temp_input_df = pd.DataFrame()
if "source_df" not in st.session_state:
    st.session_state.source_df = pd.DataFrame()


column_config_dict = {

    "Geographical (decimal degrees)":{
        "Name": st.column_config.TextColumn(
            required=True, 
            default="P001", 
            max_chars=20,
            help="Enter coordinates manually or copy/paste from table",
            validate=None,
            ),
         "Latitude": st.column_config.NumberColumn(
            required=True,
            min_value=-90.00000000, 
            max_value=90.00000000,
            default=-22.00000000,
            format="%.8f",
            help="Enter coordinates manually or copy/paste from table",
            ),
        "Longitude": st.column_config.NumberColumn(
            required=True,
            min_value=0.00000000, 
            max_value=360.00000000,
            default=16.00000000,
            format="%.8f",
            help="Enter coordinates manually or copy/paste from table",
            ),
    },

    "Geographical (deg min sec)":{
        "Name": st.column_config.TextColumn(
            required=True,
            width="small",
            default="P001", 
            max_chars=20, 
            validate=None,
            help="Enter coordinates manually or copy/paste from table",
            ),
        "Lat_deg": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=-22,
            min_value=-90, 
            max_value=90,
            format="%d",
            help="Enter coordinates manually or copy/paste from table",

            ),
        "Lat_min": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=0,
            min_value=0, 
            max_value=59,
            format="%d",
            help="Enter coordinates manually or copy/paste from table",
            ),
        "Lat_sec": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=0.00000,
            min_value=0.00000,
            max_value=59.99999,
            format="%.5f",
            help="Enter coordinates manually or copy/paste from table",
            ),
        "Lon_deg": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=16,
            min_value=0,
            max_value=360,
            format="%d",
            help="Enter coordinates manually or copy/paste from table",
            ),
        "Lon_min": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=0,
            min_value=0, 
            max_value=59,
            format="%d",
            help="Enter coordinates manually or copy/paste from table",
            ),
        "Lon_sec": st.column_config.NumberColumn(
            required=True,
            width="small",
            default=0.00000,
            min_value=0.00000,
            max_value=59.99999,
            format="%.5f",
            help="Enter coordinates manually or copy/paste from table",
            ),
    },

    "Namibian (Gauss-Conform)":{
        "Name": st.column_config.TextColumn(
            required=True, 
            default="P001", 
            max_chars=20, 
            validate=None,
            help="Enter coordinates manually or copy/paste from table",
            ),
        "y": st.column_config.NumberColumn(
            required=True,
            default=0.000,
            format="%.3f",
            help="Enter coordinates manually or copy/paste from table",
            ),
        "x": st.column_config.NumberColumn(
            required=True,
            default=0.000,
            format="%.3f",
            help="Enter coordinates manually or copy/paste from table",
            ),
    },

    "UTM":{
        "Name": st.column_config.TextColumn(
            required=True, 
            default="P001", 
            max_chars=20, 
            validate=None,
            help="Enter coordinates manually or copy/paste from table",
            ),
        "East": st.column_config.NumberColumn(
            required=True,
            default=200000.000,
            format="%.3f",
            help="Enter coordinates manually or copy/paste from table",
            ),
        "North": st.column_config.NumberColumn(
            required=True,
            default=8000000.000,
            format="%.3f",
            help="Enter coordinates manually or copy/paste from table",
            ),
    },
}

# ---- Title ---- #
st.markdown(
        '<h1 style="margin-bottom:0rem;margin-top:-5rem;text-align: left">Schwarzeck - WGS84 Transformation Namibia</h1>',
        unsafe_allow_html=True,
    )

# ---- Description and Image 2 Columns ---- #
col1a, col1b = st.columns([5, 1])
with col1a:
    st.markdown('<h5 style="color:grey;margin-bottom:0rem;margin-top:0rem;text-align: left">This app converts and transforms between different coordinate systems in the Namibian Schwarzeck datum and WGS84 datum.</h5>', unsafe_allow_html=True)
    # ---- About ---- #
    expander1 = st.expander("About this app")
    with expander1:
        st.markdown(
        """
        - **Transformation Parameters:**  
        Default Transformation is *Schwarzeck to WGS84(3)*: DX=616.8 DY=103.3 DZ=-256.9 (X-Form, Dr. Charles Merry)  
        Different transformations are selectable: *Schwarzeck to WGS84(1)* https://epsg.io/1226 or *Schwarzeck to WGS84(2)* https://epsg.io/1271
        - No warranty is given that the information provided in this app is free of errors - your use of this app and your reliance on any information on it is solely at your own risk.
        """
        ) 
        cole1,cole2=st.columns([8,1])
        cole1.markdown(
        """
        - **App by:** African Geomatics  https://www.africangeomatics.com  
        for problems and suggestions contact: s.engelhard@gmx.net
        """
        )
        cole2.image("AG_Logo_small.png")


with col1b:
    load_image()

# --------------------------------- #

# Configure sidebar
st.sidebar.subheader("View Input Coordinates on Map:")


col2a,col2b = st. columns(2)

with col2a:
    st.header("Source System")
    source_datum = st.radio(
        "Source Datum", 
        ("Schwarzeck", "WGS84"), 
        key="radio1",
        on_change=reset_dataeditor_dfs
        )
    

with col2b:
    st.header("Target System")
    col2c, col2d = st.columns([2, 3])
    with col2c:
        
        target_datum = st.radio("Target Datum", ("Schwarzeck", "WGS84"), key="radio2")

    with col2d:
        if source_datum != target_datum:
            trafo_description_dict = {
                "EPSG1226 Schwarzeck to WGS84(1)": "DX=616.0  DY=97.0  DZ=-251.0",
                "EPSG1271 Schwarzeck to WGS84(2)": "DX=615.64  DY=102.08  DZ=-255.81",
                "Default Schwarzeck to WGS84(3)": "DX=616.8  DY=103.3  DZ=-256.9",
                "EPSG1226 WGS84 to Schwarzeck(1)": "DX=-616.0  DY=-97.0  DZ=251.0",
                "EPSG1271 WGS84 to Schwarzeck(2)": "DX=-615.64  DY=-102.08  DZ=255.81",
                "Default WGS84 to Schwarzeck(3)": "DX=-616.8  DY=-103.3  DZ=256.9",
            }

            if source_datum == "Schwarzeck":
                datum_transformation = st.selectbox(
                    "Datum Transformation",
                    [
                        "EPSG1226 Schwarzeck to WGS84(1)",
                        "EPSG1271 Schwarzeck to WGS84(2)",
                        "Default Schwarzeck to WGS84(3)",
                    ],
                    index=2,
                )
            else:
                datum_transformation = st.selectbox(
                    "Datum Transformation",
                    [
                        "EPSG1226 WGS84 to Schwarzeck(1)",
                        "EPSG1271 WGS84 to Schwarzeck(2)",
                        "Default WGS84 to Schwarzeck(3)",
                    ],
                    index=2,
                )

            text_trafo_description = trafo_description_dict[datum_transformation]
            st.markdown(
                "<small style='color: #f63366'>Transformation Parameters: <br>"
                + text_trafo_description
                + "</small>",
                unsafe_allow_html=True,
            )

            trafo_Schw_WGS = Transformer.from_crs(
                trafo_dict[datum_transformation], CRS(4326), always_xy=True
            )
            trafo_WGS_Schw = Transformer.from_crs(
                CRS(4326), trafo_dict[datum_transformation], always_xy=True
            )


col3a, col3b, col3c, col3d = st.columns([3, 2, 3, 2])

with col3a:
    if source_datum == "Schwarzeck":
        source_coord_syst = st.radio(
            "Source Coordinate System",
            (
                "Geographical (decimal degrees)",
                "Geographical (deg min sec)",
                "Namibian (Gauss-Conform)",
            ),
            on_change=reset_dataeditor_dfs
        )
    else:
        source_coord_syst = st.radio(
            "Source Coordinate System",
            ("Geographical (decimal degrees)", "Geographical (deg min sec)", "UTM"),
            on_change=reset_dataeditor_dfs
        )


with col3b:
    if source_coord_syst == "Namibian (Gauss-Conform)":
        st.text(" ")
        st.text(" ")
        source_central_meridian = st.selectbox(
            "Source Projection Central Meridian",
            [11, 13, 15, 17, 18, 19, 21, 23, 25],
            index=3,
            on_change=reset_dataeditor_dfs
        )
        source_CRS = proj_dict[source_central_meridian]
    if source_coord_syst == "UTM":
        st.text(" ")
        st.text(" ")
        source_utm_zone = st.selectbox(
            "Source UTM Zone",
            ["Zone 33S (15 E)", "Zone 34S (21 E)", "Zone 35S (27 E)"],
            index=0,
            on_change=reset_dataeditor_dfs
        )
        source_CRS = utm_dict[source_utm_zone]
with col3c:
    if target_datum == "Schwarzeck":
        target_coord_syst = st.radio(
            "Target Coordinate System",
            (
                "Geographical (decimal degrees)",
                "Geographical (deg min sec)",
                "Namibian (Gauss-Conform)",
            ),
            key="target_schwarzeck",
        )
    else:
        target_coord_syst = st.radio(
            "Target Coordinate System",
            ("Geographical (decimal degrees)", "Geographical (deg min sec)", "UTM"),
            key="target_wgs",
        )

with col3d:
    if target_coord_syst == "Namibian (Gauss-Conform)":
        st.text(" ")
        st.text(" ")
        target_central_meridian = st.selectbox(
            "Target Projection Central Meridian",
            [11, 13, 15, 17, 18, 19, 21, 23, 25],
            index=3,
        )
        target_CRS = proj_dict[target_central_meridian]

    if target_coord_syst == "UTM":
        st.text(" ")
        st.text(" ")
        target_utm_zone = st.selectbox(
            "Target UTM Zone",
            ["Zone 33S (15 E)", "Zone 34S (21 E)", "Zone 35S (27 E)"],
            index=0,
        )
        target_CRS = utm_dict[target_utm_zone]

col4a, col4b = st.columns(2)

with col4a:
    
    st.markdown(
        '<h3 style="margin-bottom:0rem;margin-top:0rem;text-align: left">Source Coordinates</h3>',
        unsafe_allow_html=True,
    )
    
    st.session_state.input_method = st.radio("Select",
            ("Upload CSV File",
             "Enter Coordinates"
            ),
            label_visibility="collapsed",
            horizontal=True,
            on_change=reset_dataeditor_dfs
        )
    
    
    # Create Info Text about Source System
    if source_coord_syst == "Namibian (Gauss-Conform)":
        source_coord_syst_text = "Lo22/" + str(source_central_meridian)
    elif source_coord_syst == "Geographical (deg min sec)":
        source_coord_syst_text = "- deg min sec"
    elif source_coord_syst == "Geographical (decimal degrees)":
        source_coord_syst_text = "- decimal degrees"
    else:
        source_coord_syst_text = "UTM " + source_utm_zone[:-7]

    # CSV File
    if st.session_state.input_method == "Upload CSV File":
        # Creating example Dataframes from csv files
        if source_datum == "Schwarzeck":
            if source_coord_syst == "Geographical (deg min sec)":
                example_df = example_source_upload("dms.csv")
                example_name = "degminsec.csv"
                example_text = "Download Example CSV File - Geographical (deg min sec)"
            elif source_coord_syst == "Geographical (decimal degrees)":
                example_df = example_source_upload("dec.csv")
                example_name = "decimaldeg.csv"
                example_text = (
                    "Download Example CSV File - Geographical (decimal degrees)"
                )
            else:
                example_df = example_source_upload("Lo22" + str(source_central_meridian) + ".csv")
                example_name = "Lo22" + str(source_central_meridian) + ".csv"
                example_text = "Download Example CSV File - Namibian (Gauss-Conform)"
        else:
            if source_coord_syst == "Geographical (deg min sec)":
                example_df = example_source_upload("wgsdms.csv")
                example_name = "degminsec.csv"
                example_text = "Download Example CSV File - Geographical (deg min sec)"
            elif source_coord_syst == "Geographical (decimal degrees)":
                example_df = example_source_upload("wgsdec.csv")
                example_name = "decimaldeg.csv"
                example_text = (
                    "Download Example CSV File - Geographical (decimal degrees)"
                )
            else:
                utm_zone = source_utm_zone[5:7]
                example_df = example_source_upload("utm" + utm_zone + ".csv")
                example_name = "utm" + utm_zone + ".csv"
                example_text = "Download Example CSV File - UTM"

        # Download link for csv file according to coordinate system
        # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
        

        # Upload File
        file_check = False
        NaN_values = False
        expander2 = st.expander("Upload Coordinate File")
        uploaded_file = expander2.file_uploader(
        "Upload your coordinate file:",
        accept_multiple_files=False,
        key="upload_source_file",
        type=None,
        on_change=None,
        disabled=False,
        label_visibility="collapsed",
        )
        expander2.markdown(
            filedownload(example_df, example_name, example_text), unsafe_allow_html=True
        )
 
        if uploaded_file is not None: #checks of uploaded file
            try:
                input_df = pd.read_csv(uploaded_file)
                file_check = True
            except:
                try:
                    input_df = pd.read_csv(uploaded_file, encoding="latin-1")
                    file_check = True
                except:
                    st.warning(
                        "Error with file encoding. Please delete special characters (ä.ö,ü,...). Or try opening and saving the file in a text editor with encoding 'utf-8'."
                    )

            if file_check:
                if input_df.isnull().values.any():
                    st.warning(
                        "File contains rows with empty values, these rows were not transformed"
                    )
                    NaN_values = True

                if source_coord_syst == "Namibian (Gauss-Conform)":
                    try:
                        select = input_df[["Name", "y", "x"]]
                    except:
                        st.warning("Uploaded file must include the columns: Name, y, x")
                        file_check = False
                        input_df = example_df
                elif source_coord_syst == "Geographical (deg min sec)":
                    try:
                        select = input_df[
                            [
                                "Name",
                                "Lat_deg",
                                "Lat_min",
                                "Lat_sec",
                                "Lon_deg",
                                "Lon_min",
                                "Lon_sec",
                            ]
                        ]
                        
                    except:
                        st.warning(
                            "Uploaded file must include the columns: Name, Lat_deg, Lat_min, Lat_sec, Lon_deg, Lon_min, Lon_sec"
                        )
                        file_check = False
                        input_df = example_df
                elif source_coord_syst == "Geographical (decimal degrees)":
                    try:
                        select = input_df[["Name", "Latitude", "Longitude"]]
                        
                    except:
                        st.warning(
                            "Uploaded file must include the columns: Name, Latitude, Longitude"
                        )
                        file_check = False
                        input_df = example_df
                else:
                    try:
                        select = input_df[["Name", "East", "North"]]
                    except:
                        st.warning(
                            "Uploaded file must include the columns: Name, East, North"
                        )
                        file_check = False
                        input_df = example_df
                source_df = input_df.copy()
                if NaN_values:
                    # input_df.dropna()
                    source_df = source_df.dropna()
            else:
                input_df = example_df
                source_df = input_df.copy()

        else:
            input_df = example_df
            source_df = input_df.copy()

    
    else: # Coordinate Input

        if source_datum == "WGS84": #create example df with datum and coord syst settings and optional utm zone
            try:
                input_df = create_example_df(source_datum,source_coord_syst,source_utm_zone)
            except:
                input_df = create_example_df(source_datum,source_coord_syst)
        else: # "Schwarzeck" #create example df with datum and coord syst settings and optional central meridian
            try:
                input_df = create_example_df(source_datum,source_coord_syst,source_central_meridian)
            except:
                input_df = create_example_df(source_datum,source_coord_syst)
        
 
        temp_input_df = input_df.copy() #original input_df is saved
        st.write(source_datum + " " + source_coord_syst_text)
        edited_df = st.data_editor(
            input_df,
            key="data_editor",
            num_rows="dynamic",
            hide_index=True,
            on_change=update_editable_dataframe,
            column_config=column_config_dict[source_coord_syst]
        )
        added_rows_list = st.session_state.newdf.index.values.tolist()    
        edited_values_list = st.session_state.editeddf.index.values.tolist()
        if not len(edited_values_list) == 0: #if original input was changed
            for i in edited_values_list:
                temp_input_df.at[0,i] = st.session_state.editeddf.at[i,0]
        
        input_df = pd.concat([temp_input_df, st.session_state.newdf], axis=0)

        source_df = input_df.copy()
        file_check = True


    # Info about input received
    if st.session_state.input_method == "Upload CSV File":
        if uploaded_file is not None and file_check:
            st.write(
                "Uploaded file ("
                + source_datum
                + " "
                + source_coord_syst_text
                + "): "
                + uploaded_file.name
            )
        else:
            st.write(
                "Awaiting CSV file to be uploaded. Currently using example coordinates:"
            )
        # Display input_df
        st.dataframe(
            input_df,
            hide_index=True,
            column_config=column_config_dict[source_coord_syst]
            )
 
 
    # calculate lat long for source_df    
    if source_coord_syst == "Namibian (Gauss-Conform)":    
        trafo_yx_Schw = Transformer.from_crs(source_CRS, Schwarzeck0, always_xy=True)
        lon, lat = trafo_yx_Schw.transform(source_df["y"], source_df["x"])
        source_df["Latitude"] = lat
        source_df["Longitude"] = lon
    elif source_coord_syst == "Geographical (deg min sec)":
        source_df["Latitude"] = (
            source_df["Lat_deg"]
            - source_df["Lat_min"] / 60
            - source_df["Lat_sec"] / 3600
        )
        source_df["Longitude"] = (
            source_df["Lon_deg"]
            + source_df["Lon_min"] / 60
            + source_df["Lon_sec"] / 3600
        )
    elif source_coord_syst == "UTM":
        trafo_utm_wgs = Transformer.from_crs(source_CRS, CRS(4326), always_xy=True)
        lonw, latw = trafo_utm_wgs.transform(source_df["East"], source_df["North"])       
        source_df["Latitude"] = latw
        source_df["Longitude"] = lonw

   

    # Calculate wgs coords and display on map
    map_df = source_df.copy()
    if source_datum == "Schwarzeck":
        wgs_lon, wgs_lat = trafo_default_Schw_WGS.transform(source_df["Longitude"], source_df["Latitude"])

        map_df["latitude"] = wgs_lat
        map_df["longitude"] = wgs_lon

    else:
        map_df["latitude"] = map_df["Latitude"]
        map_df["longitude"] = map_df["Longitude"]


    if st.session_state.map_view:
        map_style="mapbox://styles/mapbox/outdoors-v11"
        button11 = st.sidebar.button(
            "Show Satellite Image", on_click=change_map_view
        )
    else:
        map_style="mapbox://styles/mapbox/satellite-streets-v11",
        button22 = st.sidebar.button(
            "Show Default Map", on_click=change_map_view
        )

    st.sidebar.pydeck_chart(
        pdk.Deck(
            map_style=map_style,
            initial_view_state=pdk.ViewState(latitude=-23, longitude=18, zoom=4),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=map_df,
                    get_position=["longitude", "latitude"],
                    get_color="[200, 30, 0, 160]",
                    radius_min_pixels=4,
                    radius_max_pixels=15,
                    pickable=True,
                    auto_highlight=True,
                )
            ],
            tooltip={"html": "<b>{Name}<b>",
                    "style": {
                        "backgroundColor": "transparent",
                        "color": "black"
                    }
            }
        )
    )



    
# Target System
with col4b:
    st.markdown(
    '<h3 style="text-align: left">Target Coordinates</h3>', unsafe_allow_html=True
    )
    st.text(" ")
    st.text(" ")
    st.text(" ")
    target_df = source_df.copy()[["Name","Latitude","Longitude"]]
    if target_coord_syst == "Namibian (Gauss-Conform)":
        target_coord_syst_text = "Lo22/" + str(target_central_meridian)
    elif target_coord_syst == "Geographical (deg min sec)":
        target_coord_syst_text = "- deg min sec"
    elif target_coord_syst == "Geographical (decimal degrees)":
        target_coord_syst_text = "- decimal degrees"
    else:
        target_coord_syst_text = "UTM " + target_utm_zone[:-7]

    if not file_check:
        st.write(
            "Awaiting file to be uploaded. Currently using example coordinates:"
        )
    else:
        st.write(target_datum + " " + target_coord_syst_text)

    # Datum Transformation
    if source_datum == "Schwarzeck" and target_datum == "WGS84":
        wgs_lon, wgs_lat = trafo_Schw_WGS.transform(source_df["Longitude"], source_df["Latitude"])
        #wgs_lon, wgs_lat = trafo_Schw_WGS.transform(source_df.iloc[: , 2], source_df.iloc[: , 1])
        target_df["Latitude"] = wgs_lat
        target_df["Longitude"] = wgs_lon

    elif source_datum == "WGS84" and target_datum == "Schwarzeck":
        schw_lon, schw_lat = trafo_WGS_Schw.transform(source_df["Longitude"], source_df["Latitude"])
        #schw_lon, schw_lat = trafo_WGS_Schw.transform(source_df.iloc[: , 2], source_df.iloc[: , 1])
        target_df["Latitude"] = schw_lat
        target_df["Longitude"] = schw_lon

    # edit target dataframe

    if target_coord_syst == "Namibian (Gauss-Conform)":

        trafo_Schw_Lo = Transformer.from_crs(Schwarzeck0, target_CRS, always_xy=True)
        y, x = trafo_Schw_Lo.transform(target_df["Longitude"], target_df["Latitude"])
        #y, x = trafo_Schw_Lo.transform(target_df.iloc[: , 2], target_df.iloc[: , 1])
        target_df["x"] = x
        target_df["y"] = y
        del target_df["Latitude"]
        del target_df["Longitude"]
        
        target_df = target_df[["Name", "y", "x"]]
        target_df = target_df.round(3)
        #st.write(target_df.style.format({"y": "{:,.3f}", "x": "{:,.3f}"}))

    elif target_coord_syst == "Geographical (deg min sec)":

        target_df["Lat_deg"] = target_df["Latitude"].astype(int)
        target_df["Lat_min_dec"] = (target_df["Lat_deg"] - target_df["Latitude"]) * 60
        target_df["Lat_min"] = target_df["Lat_min_dec"].astype(int)
        target_df["Lat_sec"] = (target_df["Lat_min_dec"] - target_df["Lat_min"]) * 60
        target_df["Lon_deg"] = target_df["Longitude"].astype(int)
        target_df["Lon_min_dec"] = (target_df["Longitude"] - target_df["Lon_deg"]) * 60
        target_df["Lon_min"] = target_df["Lon_min_dec"].astype(int)
        target_df["Lon_sec"] = (target_df["Lon_min_dec"] - target_df["Lon_min"]) * 60
        del target_df["Lat_min_dec"]
        del target_df["Lon_min_dec"]
        del target_df["Latitude"]
        del target_df["Longitude"]

        target_df = target_df[
            ["Name", "Lat_deg", "Lat_min", "Lat_sec", "Lon_deg", "Lon_min", "Lon_sec"]
        ]
        target_df = target_df.round(5)
 
    elif target_coord_syst == "Geographical (decimal degrees)":

        target_df = target_df[["Name", "Latitude", "Longitude"]]
        target_df = target_df.round(8)

    else:
        trafo_wgs_utm = Transformer.from_crs(CRS(4326), target_CRS, always_xy=True)
        east, north = trafo_wgs_utm.transform(target_df["Longitude"], target_df["Latitude"])
        #east, north = trafo_wgs_utm.transform(target_df.iloc[: , 2], target_df.iloc[: , 1])
        target_df["East"] = east
        target_df["North"] = north
        del target_df["Latitude"]
        del target_df["Longitude"]

        target_df = target_df[["Name", "East", "North"]]
        target_df = target_df.round(3)
 

    st.dataframe(
        target_df,
        hide_index=True,
        column_config=column_config_dict[target_coord_syst]
        )

    # define file download name
    if target_coord_syst == "Namibian (Gauss-Conform)":
        output_name = "Lo22" + str(target_central_meridian) + ".csv"
        output_text = "Download Output File - Namibian (Gauss-Conform)"
    elif target_coord_syst == "Geographical (deg min sec)":
        output_name = "degminsec.csv"
        output_text = "Download Output File - Geographical (deg min sec)"
    elif target_coord_syst == "Geographical (decimal degrees)":
        output_name = "decimaldeg.csv"
        output_text = "Download Output File - Geographical (decimal degrees)"
    else:
        output_name = "utm" + target_utm_zone[5:7] + ".csv"
        output_text = "Download Output File - UTM"

    # target file download
    st.markdown(
        filedownload(target_df, output_name, output_text), unsafe_allow_html=True
    )
