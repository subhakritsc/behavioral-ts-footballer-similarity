# Player Similarity Dashboard

An interactive dashboard to visualize and compare football players based on their behavioral time-series data using Dynamic Time Warping (DTW) similarity.

## Direct Installation (Bash)

Copy and paste these commands into your terminal to get started immediately:

```bash
# 1. Clone & Enter Directory
git clone https://github.com/subhakritsc/behavioral-ts-footballer-similarity.git
cd behavioral-ts-footballer-similarity

# 2. Install Dependencies (including gdown for Google Drive)
pip install streamlit pandas matplotlib gdown

# 3. Download the Dataset from Google Drive
# NOTE: gdown creates a folder. We move files out so app.py can find them.
gdown --folder 1wAz7XDkakamk8NufsGW1lhy1spV2w_hL
mv */*.csv . 2>/dev/null || true
# 4. Run the Application
streamlit run app.py
```

## Dashboard Features
- **Player Discovery:** Select any player to see their behavioral "twins".
- **Similarity Score:** Uses DTW to match players with similar movement and intensity profiles.
- **Visual Analysis:** Compare touches, passes, and average position trends over 90 minutes.

---
*Data Source: Based on StatsBomb Open Data (2015/16 Premier League Season).*
