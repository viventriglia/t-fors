from pathlib import Path
from PIL import Image

APP_VERSION = "0.2.1"

# Data/images/model
DATA_PATH = Path(Path(__file__).parents[1], "data", "out")
IMAGES_PATH = Path(Path(__file__).parents[1], "images", "app")
FAVICON = Image.open(Path(IMAGES_PATH, "favicon.png"))
LOGO = Image.open(Path(IMAGES_PATH, "logo.png"))
EU_LOGO_NEG = Image.open(Path(IMAGES_PATH, "funded_by_the_EU_RGB_neg.png"))
EU_LOGO_WHT = Image.open(Path(IMAGES_PATH, "funded_by_the_EU_RGB_white_outline.png"))
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

# Human-readable variable names
VAR_NAMES_DICT = {
    "ie_fix": "Auroral electrojet (IE index)",
    "ie_variation": "Auroral electrojet (IE index variation)",
    "ie_mav_3h": "Auroral electrojet (IE index, 3h moving average)",
    "ie_mav_6h": "Auroral electrojet (IE index, 6h moving average)",
    "ie_mav_12h": "Auroral electrojet (IE index, 12h moving average)",
    "ie_mav_24h": "Auroral electrojet (IE index, 24h moving average)",
    "iu_fix": "Auroral electrojet (IU index)",
    "iu_variation": "Auroral electrojet (IU index variation)",
    "iu_mav_3h": "Auroral electrojet (IU index, 3h moving average)",
    "iu_mav_6h": "Auroral electrojet (IU index, 6h moving average)",
    "iu_mav_12h": "Auroral electrojet (IU index, 12h moving average)",
    "iu_mav_24h": "Auroral electrojet (IU index, 24h moving average)",
    "hf": "HF-EU index",
    "hf_mav_2h": "HF-EU index (2h moving average)",
    "f_107_adj": "F10.7",
    "hp_30": "HP-30",
    "smr": "SMR (ring current)",
    "solar_zenith_angle": "Solar Zenith Angle",
    "newell": "Newell index",
    "local_warning_level_at": "Local warning level (Athens)",
    "local_warning_level_ff": "Local warning level (Fairford)",
    "local_warning_level_jr": "Local warning level (Juliusruh)",
    "local_warning_level_pq": "Local warning level (Průhonice)",
    "local_warning_level_ro": "Local warning level (Rome)",
    "local_warning_level_vt": "Local warning level (San Vito)",
    "spectral_contribution_at": "Spectral contribution (Athens)",
    "spectral_contribution_ff": "Spectral contribution (Fairford)",
    "spectral_contribution_jr": "Spectral contribution (Juliusruh)",
    "spectral_contribution_pq": "Spectral contribution (Průhonice)",
    "spectral_contribution_ro": "Spectral contribution (Rome)",
    "spectral_contribution_vt": "Spectral contribution (San Vito)",
    "azimuth_at": "Azimuth (Athens)",
    "azimuth_ff": "Azimuth (Fairford)",
    "azimuth_jr": "Azimuth (Juliusruh)",
    "azimuth_pq": "Azimuth (Průhonice)",
    "azimuth_ro": "Azimuth (Rome)",
    "azimuth_vt": "Azimuth (San Vito)",
    "velocity_at": "Velocity (Athens)",
    "velocity_ff": "Velocity (Fairford)",
    "velocity_jr": "Velocity (Juliusruh)",
    "velocity_pq": "Velocity (Průhonice)",
    "velocity_ro": "Velocity (Rome)",
    "velocity_vt": "Velocity (San Vito)",
    "true": "Target",
    "pred": "Vanilla prediction",
    "pred_proba": "Class score",
    "pred_f1_max": "Max F1-score prediction",
    "pred_p_80": "High-precision prediction",
    "pred_r_60": "High-recall prediction",
}

VAR_NAMES_INVERSE_DICT = {v: k for k, v in VAR_NAMES_DICT.items()}
