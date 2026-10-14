import streamlit as st
import pandas as pd

# Load player statistics
player_stats = pd.read_csv("player_stats.csv", index_col=0)

st.title("🏏 CricketIQ")
st.write("Cricket Player Performance Analyzer")

st.header("Player Comparison")

# Player selection
players = sorted(player_stats.index.tolist())

player1 = st.selectbox(
    "Select Player 1",
    players,
    index=players.index("V Kohli")
)

player2 = st.selectbox(
    "Select Player 2",
    players,
    index=players.index("RG Sharma")
)

# Show selected player statistics

st.subheader("Head-to-Head Comparison")

# Display key statistics as comparison cards
metric_columns = st.columns(3)

metrics = [
    ("Runs", "Runs"),
    ("Batting Average", "Batting Average"),
    ("Strike Rate", "Strike Rate")
]

for col, (label, column_name) in zip(metric_columns, metrics):
    with col:
        st.write(f"**{label}**")
        st.metric(
            player1,
            f"{player_stats.loc[player1, column_name]:,.2f}"
            if column_name != "Runs"
            else f"{player_stats.loc[player1, column_name]:,.0f}"
        )
        st.metric(
            player2,
            f"{player_stats.loc[player2, column_name]:,.2f}"
            if column_name != "Runs"
            else f"{player_stats.loc[player2, column_name]:,.0f}"
        )

# Full comparison table
comparison = pd.DataFrame({
    "Statistic": player_stats.columns,
    player1: player_stats.loc[player1].values,
    player2 if player2 != player1 else f"{player2} (Player 2)": player_stats.loc[player2].values
})

st.dataframe(comparison, hide_index=True, use_container_width=True)


st.subheader("📊 Runs Comparison")

runs_chart = pd.DataFrame({
    "Player": [player1, player2],
    "Runs": [
        player_stats.loc[player1, "Runs"],
        player_stats.loc[player2, "Runs"]
    ]
})

st.bar_chart(runs_chart, x="Player", y="Runs")

st.subheader("📈 Batting Efficiency Comparison")

efficiency_chart = pd.DataFrame({
    "Player": [player1, player2],
    "Batting Average": [
        player_stats.loc[player1, "Batting Average"],
        player_stats.loc[player2, "Batting Average"]
    ],
    "Strike Rate": [
        player_stats.loc[player1, "Strike Rate"],
        player_stats.loc[player2, "Strike Rate"]
    ]
})


st.write("**Batting Average**")
st.bar_chart(
    efficiency_chart,
    x="Player",
    y="Batting Average"
)

st.write("**Strike Rate**")
st.bar_chart(
    efficiency_chart,
    x="Player",
    y="Strike Rate"
)


st.header("🏆 Player Leaderboard")

leaderboard_metric = st.selectbox(
    "Rank players by",
    ["Runs", "Batting Average", "Strike Rate", "Matches"]
)

leaderboard = player_stats.sort_values(
    by=leaderboard_metric,
    ascending=False
).head(10)

st.dataframe(
    leaderboard,
    use_container_width=True
)


st.header("🔎 Explore a Player")

searched_player = st.selectbox(
    "Choose a player to explore",
    sorted(player_stats.index.tolist()),
    key="profile_player"
)

st.subheader(f"📋 {searched_player} — Career Profile")

profile = player_stats.loc[searched_player]

col1, col2, col3 = st.columns(3)

col1.metric("Runs", f"{profile['Runs']:,.0f}")
col2.metric("Batting Average", f"{profile['Batting Average']:.2f}")
col3.metric("Strike Rate", f"{profile['Strike Rate']:.2f}")

col4, col5, col6 = st.columns(3)

col4.metric("Matches Batted", f"{profile['Matches']:,.0f}")
col5.metric("Balls Faced", f"{profile['Balls Faced']:,.0f}")
col6.metric("Dismissals", f"{profile['Dismissals']:,.0f}")

