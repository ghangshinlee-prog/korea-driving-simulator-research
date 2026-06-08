"""
Configuration for the driver vision-workload analysis (M.S. thesis extension).

The M.S. thesis "Development of Driving Vision-Workload Measures to Evaluate
Safety Level" (University of Seoul, 2023) developed eye-tracking based measures
of driver visual/cognitive workload. This module supports an analysis angle not
covered in the companion toll-plaza repo: how those measures vary by driver
**age group** and **gender** — directly relevant to evaluating safety risk.

Paths resolve from DATA_DIR (default ./data); raw data is not committed (DATA.md).
"""
from pathlib import Path
import os

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))
REPO_DIR = Path(__file__).resolve().parent.parent
FIG_DIR = REPO_DIR / "figures"
RESULT_DIR = REPO_DIR / "results"
FIG_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)

EYE_PATH = DATA_DIR / "vision_workload_events.tsv"

AGE_ORDER = [30, 40, 50]
GENDERS = ["Male", "Female"]
AGE_COLORS = {30: "#4cc9f0", 40: "#ff9f1c", 50: "#f72585"}   # accent palette
GENDER_COLORS = {"Male": "#4361ee", "Female": "#f72585"}
SIG = 0.05


def style_pub(plt):
    plt.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "axes.edgecolor": "#333333",
        "axes.grid": True, "grid.color": "#e6e6e6", "grid.linewidth": 0.8,
        "axes.axisbelow": True, "font.size": 12, "axes.titlesize": 15,
        "axes.titleweight": "bold", "figure.dpi": 110,
    })
