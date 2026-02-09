import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

FEATURES = [
    "touches",
    "passes",
    "carries",
    "defensive_actions",
    'avg_x',
    'avg_y'
]

@st.cache_data
def load_data():
    ts = pd.read_csv("player_timeseries.csv")
    pos = pd.read_csv("positions.csv")
    top3 = pd.read_csv("top3_similarity.csv")
    return ts, pos, top3


# ===== Utilities =====
def get_ts(df, player):
    p = df[df.player == player]

    # เติม minute ให้ครบเพื่อให้กราฟไม่ขาด
    full = pd.DataFrame({"minute_bin": range(1, 91)})
    p = full.merge(p, on="minute_bin", how="left")
    p[FEATURES] = p[FEATURES].fillna(0)

    return p.sort_values("minute_bin")


def plot_compare(ts_df, p1, p2, feature):
    d1 = get_ts(ts_df, p1)
    d2 = get_ts(ts_df, p2)

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(d1["minute_bin"], d1[feature], label=p1)
    ax.plot(d2["minute_bin"], d2[feature], label=p2)

    ax.set_title(feature)
    ax.set_xlabel("Minute")
    ax.legend()

    st.pyplot(fig)


# ===== Load =====
ts_df, pos_df, top3_df = load_data()

players = sorted(pos_df["player"].unique())
player_pos_map = dict(zip(pos_df["player"], pos_df["position"]))


def format_func(player_name):
    return f"{player_name} ({player_pos_map.get(player_name, 'Unknown')})"


st.title("Player Similarity via Behavioral Time Series")

col1, col2 = st.columns([1, 2])

# ===== Left Panel =====
with col1:
    selected_player = st.selectbox(
        "Select Player",
        players,
        format_func=format_func
    )

    sims = top3_df[top3_df.player == selected_player]

    st.subheader("Top 3 Similar Players")

    sim_players = []
    for _, row in sims.iterrows():
        sp = row["similar_player"]
        sim_players.append(sp)

        pos = player_pos_map.get(sp, "Unknown")
        st.write(f"- {sp} ({pos})")


# ===== Right Panel =====
with col2:
    if len(sim_players) > 0:
        selected_b = st.selectbox(
            "Compare with (Top 3 only)",
            sim_players,
            format_func=format_func
        )

        feature = st.selectbox("Select Feature to Compare", FEATURES)

        pos_a = player_pos_map.get(selected_player, "Unknown")
        pos_b = player_pos_map.get(selected_b, "Unknown")

        st.markdown(f"### {selected_player} ({pos_a}) vs {selected_b} ({pos_b})")

        plot_compare(ts_df, selected_player, selected_b, feature)
