from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class InputDataModel(BaseModel):
    """(Pydantic-based) schema of model input data"""

    ie_fix: Optional[float] = Field(
        description="Auroral-zone magnetic activity produced by enhanced ionospheric currents flowing below and within the auroral oval in the sector covered by the FMI-IMAGE magnetometer network"
    )
    ie_variation: Optional[int] = Field(
        description="Change in the IE index (increase, decrease, stationary)"
    )
    ie_mav_3h: Optional[float] = Field(
        description="IE exponential moving averages within 3-hours window"
    )
    ie_mav_12h: Optional[float] = Field(
        description="IE exponential moving averages within 12-hours window"
    )
    iu_fix: Optional[float] = Field(
        description="Strongest current intensities of the eastward auroral electrojets in the sector covered by the FMI-IMAGE magnetometer network"
    )
    iu_variation: Optional[int] = Field(
        description="Change in the IE index (increase, decrease, stationary)"
    )
    iu_mav_3h: Optional[float] = Field(
        description="IE exponential moving averages within 3-hours window"
    )
    iu_mav_12h: Optional[float] = Field(
        description="IE exponential moving averages within 12-hours window"
    )
    hf: Optional[float] = Field(
        description="High-Frequency interferometry (HF-INT) index, identifying activity over the European network of ionosondes"
    )
    hf_mav_2h: Optional[float] = Field(
        description="HF-INT exponential moving averages within 2-hours window"
    )
    f_107_adj: Optional[float] = Field(
        description="Solar radio flux at 10.7 cm (2800 MHz)"
    )
    hp_30: Optional[float] = Field(description="Half-hourly geomagnetic index")
    dst: Optional[float] = Field(
        description="Disturbance-storm-time index, a measure of the severity of the geomagnetic storm"
    )
    solar_zenith_angle: Optional[float] = Field(
        description="Angle between the local zenith (i.e. directly above the point on the ground) and the line of sight from that point to the Sun"
    )
    newell: Optional[float] = Field(
        description="Coupling function which quantifies the energy transfer from the magnetosphere to the ionosphere"
    )
    bz: Optional[float] = Field(
        description="Strength of the interplanetary magnetic field in a north/south direction"
    )
    speed: Optional[float] = Field(description="Solar wind flux radial velocity")
    rho: Optional[float] = Field(description="Solar wind flux density")
    spectral_contribution_at: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Athens)"
    )
    spectral_contribution_ff: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Fairford)"
    )
    spectral_contribution_jr: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Juliusruh)"
    )
    spectral_contribution_pq: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Průhonice)"
    )
    spectral_contribution_ro: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Rome)"
    )
    spectral_contribution_vt: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (San Vito)"
    )
    azimuth_at: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Athens)"
    )
    azimuth_ff: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Fairford)"
    )
    azimuth_jr: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Juliusruh)"
    )
    azimuth_pq: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Průhonice)"
    )
    azimuth_ro: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Rome)"
    )
    azimuth_vt: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (San Vito)"
    )
    velocity_at: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Athens)"
    )
    velocity_ff: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Fairford)"
    )
    velocity_jr: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Juliusruh)"
    )
    velocity_pq: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Průhonice)"
    )
    velocity_ro: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Rome)"
    )
    velocity_vt: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (San Vito)"
    )


class OutputDataModel(BaseModel):
    """(Pydantic-based) schema of model output"""

    datetime_ref: datetime = Field(
        description="Reference date and time (UTC) for the data used by the model"
    )
    datetime_run: datetime = Field(description="Date and time (UTC) of model run")
    prediction_score: float = Field(
        description="Raw model score, where a higher one means the model is more confident in its prediction; this score is related to the probability of an observation belonging to the positive class (LSTID in the following 3 hrs)"
    )
    prediction_hprec: int = Field(
        description="Binary output of the model with decision threshold set to 0.84, in order to achieve 80%-level precision"
    )
    prediction_balan: int = Field(
        description="Binary output of the model with decision threshold set to 0.64 (mean cross-validated F1-score: 0.55)"
    )
    prediction_hsens: int = Field(
        description="Binary output of the model with decision threshold set to 0.48, in order to achieve 60%-level recall"
    )
    ie_fix: Optional[float] = Field(
        description="Auroral-zone magnetic activity produced by enhanced ionospheric currents flowing below and within the auroral oval in the sector covered by the FMI-IMAGE magnetometer network"
    )
    ie_variation: Optional[int] = Field(
        description="Change in the IE index (increase, decrease, stationary)"
    )
    ie_mav_3h: Optional[float] = Field(
        description="IE exponential moving averages within 3-hours window"
    )
    ie_mav_12h: Optional[float] = Field(
        description="IE exponential moving averages within 12-hours window"
    )
    iu_fix: Optional[float] = Field(
        description="Strongest current intensities of the eastward auroral electrojets in the sector covered by the FMI-IMAGE magnetometer network"
    )
    iu_variation: Optional[int] = Field(
        description="Change in the IE index (increase, decrease, stationary)"
    )
    iu_mav_3h: Optional[float] = Field(
        description="IE exponential moving averages within 3-hours window"
    )
    iu_mav_12h: Optional[float] = Field(
        description="IE exponential moving averages within 12-hours window"
    )
    hf: Optional[float] = Field(
        description="High-Frequency interferometry (HF-INT) index, identifying activity over the European network of ionosondes"
    )
    hf_mav_2h: Optional[float] = Field(
        description="HF-INT exponential moving averages within 2-hours window"
    )
    f_107_adj: Optional[float] = Field(
        description="Solar radio flux at 10.7 cm (2800 MHz)"
    )
    hp_30: Optional[float] = Field(description="Half-hourly geomagnetic index")
    dst: Optional[float] = Field(
        description="Disturbance-storm-time index, a measure of the severity of the geomagnetic storm"
    )
    solar_zenith_angle: Optional[float] = Field(
        description="Angle between the local zenith (i.e. directly above the point on the ground) and the line of sight from that point to the Sun"
    )
    newell: Optional[float] = Field(
        description="Coupling function which quantifies the energy transfer from the magnetosphere to the ionosphere"
    )
    bz: Optional[float] = Field(
        description="Strength of the interplanetary magnetic field in a north/south direction"
    )
    speed: Optional[float] = Field(description="Solar wind flux radial velocity")
    rho: Optional[float] = Field(description="Solar wind flux density")
    spectral_contribution_at: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Athens)"
    )
    spectral_contribution_ff: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Fairford)"
    )
    spectral_contribution_jr: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Juliusruh)"
    )
    spectral_contribution_pq: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Průhonice)"
    )
    spectral_contribution_ro: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (Rome)"
    )
    spectral_contribution_vt: Optional[float] = Field(
        description="Spectral energy contribution (%) of the perturbation (San Vito)"
    )
    azimuth_at: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Athens)"
    )
    azimuth_ff: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Fairford)"
    )
    azimuth_jr: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Juliusruh)"
    )
    azimuth_pq: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Průhonice)"
    )
    azimuth_ro: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (Rome)"
    )
    azimuth_vt: Optional[float] = Field(
        description="Azimuth (degrees from true North) of the perturbation (San Vito)"
    )
    velocity_at: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Athens)"
    )
    velocity_ff: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Fairford)"
    )
    velocity_jr: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Juliusruh)"
    )
    velocity_pq: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Průhonice)"
    )
    velocity_ro: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (Rome)"
    )
    velocity_vt: Optional[float] = Field(
        description="Velocity (m/s) of the perturbation (San Vito)"
    )
