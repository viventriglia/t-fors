from pathlib import Path
from PIL import Image

APP_VERSION = "0.1.1"

# Data/images/model
DATA_PATH = Path("..", "data", "out")
FAVICON = Image.open(Path("..", "images", "favicon.png"))
MODEL_PATH = Path(
    "..",
    "mlruns",
    "836438889763744696",
    "bfb81fc4f057443eaa8aaf808d39951c",
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
