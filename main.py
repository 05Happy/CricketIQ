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
    21: "match_id"
})


# Convert numerical columns
all_df["batter_runs"] = pd.to_numeric(all_df["batter_runs"])
all_df["extras"] = pd.to_numeric(all_df["extras"])


print("\nAll IPL data loaded!")
print("Total deliveries:", len(all_df))


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


print("\nTop 20 Players by Matches Played:")
print(matches_played.head(20))