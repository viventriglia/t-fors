from pathlib import Path
from PIL import Image

APP_VERSION = "0.2.3"

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
    "47379e58abff4b18989898a5b6ecbe08",
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
    # "ie_mav_6h": "Auroral electrojet (IE index, 6h moving average)",
    "ie_mav_12h": "Auroral electrojet (IE index, 12h moving average)",
    # "ie_mav_24h": "Auroral electrojet (IE index, 24h moving average)",
    "iu_fix": "Auroral electrojet (IU index)",
    "iu_variation": "Auroral electrojet (IU index variation)",
    "iu_mav_3h": "Auroral electrojet (IU index, 3h moving average)",
    # "iu_mav_6h": "Auroral electrojet (IU index, 6h moving average)",
    "iu_mav_12h": "Auroral electrojet (IU index, 12h moving average)",
    # "iu_mav_24h": "Auroral electrojet (IU index, 24h moving average)",
    "hf": "HF-EU index",
    "hf_mav_2h": "HF-EU index (2h moving average)",
    "f_107_adj": "F10.7",
    "hp_30": "HP-30",
    "smr": "SMR (ring current)",
    "solar_zenith_angle": "Solar Zenith Angle",
    "newell": "Newell index",
    "rho": "ρ (solar wind density)",  # "Solar wind flux density",
    "vx": "vx (solar wind velocity)",  # "Solar wind flux radial velocity",
    "bz": "Bz (interplanetary magnetic field)",  # "Strength of the interplanetary magnetic field in a north/south direction",
    # "local_warning_level_at": "Local warning level (Athens)",
    # "local_warning_level_ff": "Local warning level (Fairford)",
    # "local_warning_level_jr": "Local warning level (Juliusruh)",
    # "local_warning_level_pq": "Local warning level (Průhonice)",
    # "local_warning_level_ro": "Local warning level (Rome)",
    # "local_warning_level_vt": "Local warning level (San Vito)",
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
    # "pred": "Vanilla prediction",
    "pred_proba": "Class score",
    "pred_f1_max": "Balanced prediction",
    "pred_p_80": "High-precision prediction",
    "pred_r_60": "High-recall prediction",
}
VAR_NAMES_INVERSE_DICT = {v: k for k, v in VAR_NAMES_DICT.items()}
FEAT_NAMES_DICT = {
    "Auroral electrojet (IE) index": "Provides a measure of auroral-zone magnetic activity produced by enhanced ionospheric currents flowing below and within the auroral oval in the sector covered by the FMI-IMAGE magnetometer network",
    "Auroral electrojet (IE) variation": "Change in the IE index (increase, decrease, stationary)",
    "Auroral electrojet (IE) moving averages": "IE exponential moving averages within 3- and 12-hours window",
    "Auroral electrojet (IU) index": "Measures the strongest current intensities of the eastward auroral electrojets in the sector covered by the FMI-IMAGE magnetometer network",
    "Auroral electrojet (IU) variation": "Change in the IU index (increase, decrease, stationary)",
    "Auroral electrojet (IU) moving averages": "IU exponential moving averages within 3- and 12-hours window",
    "HF-EU index": "High-Frequency interferometry index, identifying activity over the European network of ionosondes",
    "HF-EU index (2h moving average)": "HF-EU exponential moving averages within 2-hours window",
    "F10.7": "Solar radio flux at 10.7 cm (2800 MHz)",
    "HP-30": "Half-hourly geomagnetic index",
    "SMR (ring current)": "SuperMAG partial ring current index",
    "Solar Zenith Angle": "Angle between the local zenith (i.e. directly above the point on the ground) and the line of sight from that point to the Sun",
    "Newell index": "Coupling function which quantifies the energy transfer from the magnetosphere to the ionosphere",
    "ρ (solar wind density)": "Solar wind flux density",
    "vx (solar wind velocity)": "Solar wind flux radial velocity",
    "Bz (interplanetary magnetic field)": "Strength of the interplanetary magnetic field in a north/south direction",
    # "Local warning level (Athens, Juliusruh, Průhonice, Rome, San Vito)": "Discrete variable representing the reported level of activity (one feature per ionosonde)",
    "Spectral contribution (Athens, Juliusruh, Průhonice, Rome, San Vito)": "Spectral energy contribution (%) of the perturbation (one feature per ionosonde)",
    "Azimuth (Athens, Juliusruh, Průhonice, Rome, San Vito)": "Azimuth (degrees from true North) of the perturbation (one feature per ionosonde)",
    "Velocity (Athens, Juliusruh, Průhonice, Rome, San Vito)": "Velocity (m/s) of the perturbation (one feature per ionosonde)",
}
OUTP_NAMES_DICT = {
    "Target": "Discrete variable, derived from the LSTID catalogue; it is 1 if there is an LSTID event within 3 hours, 0 otherwise",
    "Class score": "Soft classification gives scores, where a higher score for that class means the model is more confident in its prediction; this score is related to the probability of an observation belonging to, say, the positive class (LSTID occurs)",
    # "Vanilla prediction": "Binary output of the model with decision threshold set to the “standard” value of 0.50 (cross-validated F1-score: 0.54)",
    "Balanced prediction": "Binary output of the model with decision threshold set to 0.68 (mean cross-validated F1-score: 0.56)",
    "High-precision prediction": "Binary output of the model with decision threshold set to 0.85 (mean cross-validated F1-score: 0.50), in order to achieve 80%-level precision",
    "High-sensitivity prediction": "Binary output of the model with decision threshold set to 0.54 (mean cross-validated F1-score: 0.55), in order to achieve 60%-level recall",
}
