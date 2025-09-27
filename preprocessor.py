import random
import pandas as pd

# pehle sirf column names lo
df_head = pd.read_csv("US_Accidents_March23.csv", nrows=0)

# saari rows load karne ki zarurat nahi, line count kar ke sample karo
n_rows = sum(1 for _ in open("US_Accidents_March23.csv")) - 1  # minus header
skip = sorted(random.sample(range(1, n_rows+1), n_rows - 1_000_000))

df = pd.read_csv("US_Accidents_March23.csv", skiprows=skip)