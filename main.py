import pandas as pd
import glob
import csv

# -----------------------------------
# 1. Find all IPL match files
# -----------------------------------

files = glob.glob("data/*.csv")

print("Number of match files:", len(files))


# -----------------------------------
# 2. Read all IPL deliveries
# -----------------------------------

all_matches = []

for file in files:

    with open(file, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    # Find where ball-by-ball data starts
    ball_start = None

    for i, row in enumerate(rows):
        if row and row[0] == "ball":
            ball_start = i + 1
            break

    # Find match ID
    match_id = None

    for row in rows:
        if len(row) >= 3 and row[0] == "info" and row[1] == "match_id":
            match_id = row[2]
            break

    # Store every delivery
    for row in rows[ball_start:]:
        if row and row[0] == "ball":

            # Add match ID
            row.append(match_id)

            all_matches.append(row)


print("Total deliveries across IPL:")
print(len(all_matches))


# -----------------------------------
# 3. Convert data into Pandas DataFrame
# -----------------------------------

all_df = pd.DataFrame(all_matches)


all_df = all_df.rename(columns={
    0: "type",
    1: "innings",
    2: "over_ball",
    3: "batting_team",
    4: "batter",
    5: "non_striker",
    6: "bowler",
    7: "batter_runs",
    8: "extras",
    9: "wides",
    10: "noballs",
    11: "byes",
    12: "legbyes",
    13: "penalty",
    14: "dismissal_method",
    15: "dismissed_players",
    16: "actual_delivery",
    17: "non_boundary",
    18: "fielder_1",
    19: "fielder_2",
    20: "fielder_3",
    21: "match_id"
})


# Convert numerical columns
all_df["batter_runs"] = pd.to_numeric(all_df["batter_runs"])
all_df["extras"] = pd.to_numeric(all_df["extras"])

# Check dismissal types
print("\nDismissal types in dataset:")
print(
    all_df.loc[
        all_df["dismissal_method"] != "",
        "dismissal_method"
    ].value_counts()
)



# -----------------------------------
# 4. Total runs by player
# -----------------------------------

player_runs = (
    all_df.groupby("batter")["batter_runs"]
    .sum()
    .sort_values(ascending=False)
)


print("\nTop 20 IPL Run Scorers:")
print(player_runs.head(20))


# -----------------------------------
# 5. Matches played by each player
# -----------------------------------

matches_played = (
    all_df.groupby("batter")["match_id"]
    .nunique()
    .sort_values(ascending=False)
)


print("\nTop 20 Players by Matches Batted:")
print(matches_played.head(20))

# -----------------------------------
# 6. Balls faced
# -----------------------------------

# A wide is not counted as a ball faced.
# No-balls ARE counted as balls faced.

balls_faced = (
    all_df[all_df["wides"] == ""]
    .groupby("batter")
    .size()
)

# -----------------------------------
# 6B. Times dismissed
# -----------------------------------

# Dismissals that count against batting average
excluded_dismissals = [
    "retired hurt",
]

dismissals = (
    all_df[
        (all_df["dismissal_method"] != "") &
        (~all_df["dismissal_method"].str.lower().isin(
            excluded_dismissals
        ))
    ]["dismissed_players"]
    .dropna()
    .str.split("&")
    .explode()
    .str.strip()
    .loc[lambda s: s != ""]
    .value_counts()
)

print("\nSample dismissed-player values:")
print(
    all_df.loc[
        all_df["dismissal_method"] != "",
        "dismissed_players"
    ].dropna().head(15).tolist()
)

print("\nTop 10 Players by Dismissals:")
print(dismissals.sort_values(ascending=False).head(10))


# -----------------------------------
# 7. Strike rate
# -----------------------------------

strike_rate = (
    player_runs.div(balls_faced.replace(0, float("nan"))) * 100
).round(2)

strike_rate = strike_rate.sort_values(ascending=False)

print("\nTop 20 Players by Strike Rate:")
print(strike_rate.head(20))

# -----------------------------------
# 8. Strike rate leaderboard
# -----------------------------------

minimum_balls = 500

qualified_players = balls_faced[balls_faced >= minimum_balls].index

qualified_strike_rate = (
    strike_rate.loc[qualified_players]
    .sort_values(ascending=False)
)


print("\nTop 20 IPL Players by Strike Rate (500+ balls):")
print(qualified_strike_rate.head(20))



# -----------------------------------
# Player Statistics Table
# -----------------------------------


player_stats = pd.DataFrame({
    "Runs": player_runs,
    "Matches": matches_played,
    "Balls Faced": balls_faced,
    "Dismissals": dismissals,
    "Strike Rate": strike_rate
})

player_stats["Dismissals"] = player_stats["Dismissals"].fillna(0)

player_stats["Batting Average"] = (
    player_stats["Runs"] /
    player_stats["Dismissals"].replace(0, float("nan"))
).round(2)


player_stats = player_stats.fillna(0)

print("\nPlayer Statistics:")
print(player_stats.head(20))

# -----------------------------------
# Player Search
# -----------------------------------

player = "V Kohli"

if player in player_stats.index:
    print("\nPlayer Profile:")
    print(player_stats.loc[player])
else:
    print("Player not found")



# Save player statistics
player_stats.to_csv("player_stats.csv", index="True")


from collections import Counter

match_dates = []

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) >= 3 and row[0] == "info" and row[1] == "date":
                match_dates.extend(value for value in row[2:] if value)
                break

print("\nDataset date coverage:")
print("Earliest date:", min(match_dates))
print("Latest date:", max(match_dates))
print("Total dated matches:", len(match_dates))

year_counts = Counter(date[:4] for date in match_dates)

print("\nMatches by year:")
for year in sorted(year_counts):
    print(f"{year}: {year_counts[year]} matches")

