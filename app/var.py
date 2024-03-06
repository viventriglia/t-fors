from pathlib import Path
from PIL import Image

APP_VERSION = "0.2.0"

# Data/images/model
DATA_PATH = Path(Path(__file__).parents[1], "data", "out")
FAVICON_PATH = Path(Path(__file__).parents[1], "images", "favicon.png")
FAVICON = Image.open(FAVICON_PATH)
MODEL_PATH = Path(
    Path(__file__).parents[1],
    "mlruns",
    "836438889763744696",
    "ed451d15e8094aa593f44d07bc77696d",
    "artifacts",
    "model",
    "model.cb",
)

# Streamlit/Plotly vars
GLOBAL_STREAMLIT_STYLE = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .css-15zrgzn {display: none}
            </style>
            """
PLT_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToAdd": [
        "drawline",
        "drawopenpath",
        "drawcircle",
        "drawrect",
        "eraseshape",
    ],
    "scrollZoom": False,
}
PLT_CONFIG_NO_LOGO = {"displaylogo": False}
CACHE_EXPIRE_SECONDS = 600
PLT_FONT_SIZE = 16
