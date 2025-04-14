import pandas as pd

mhi_data = pd.read_csv("CENSUS_MHI_STATE.csv")
population_data = pd.read_csv("CENSUS_POPULATION_STATE.csv")
state_keys = pd.read_csv("KEYS.csv")
redfin_data = pd.read_csv("REDFIN_MEDIAN_SALE_PRICE.csv")

state_abbreviations = state_keys["state_abbreviation"].unique().tolist()
state_abbreviations = [state.strip().upper() for state in state_abbreviations]

print(f"States from KEYS: {state_abbreviations}")
print(f"States in MHI data columns: {mhi_data.columns}")
print(f"States in Population data columns: {population_data.columns}")
print(f"States in Redfin data columns: {redfin_data.columns}")

mhi_incomes = {}
for state in state_abbreviations:
    column_name = f"{state}!!Median income (dollars)!!Estimate"
    if column_name in mhi_data.columns:
        mhi_incomes[state] = mhi_data[column_name].iloc[0]
    else:
        print(f"Column for {state} not found in MHI data.")

mhi_clean = pd.DataFrame(list(mhi_incomes.items()), columns=["State", "2022 MHI"])
print(f"MHI Data:\n{mhi_clean.head()}")

population_estimates = {}
for state in state_abbreviations:
    column_name = f"{state}!!Estimate"
    if column_name in population_data.columns:
        population_estimates[state] = population_data[column_name].iloc[0]
    else:
        print(f"Column for {state} not found in Population data.")

population_clean = pd.DataFrame(list(population_estimates.items()), columns=["State", "2022 Population"])
print(f"Population Data:\n{population_clean.head()}")

redfin_latest = redfin_data.iloc[-1, 1:].reset_index(drop=True)
redfin_clean = pd.DataFrame({
    "State": redfin_data.columns[1:],
    "2022 Median Sale Price": redfin_latest
})

redfin_clean["State"] = redfin_clean["State"].str.strip()

print(f"Redfin Data:\n{redfin_clean.head()}")

mhi_clean["State"] = mhi_clean["State"].str.strip()
population_clean["State"] = population_clean["State"].str.strip()
redfin_clean["State"] = redfin_clean["State"].str.strip()

merged_data = mhi_clean.merge(population_clean, on="State", how="outer")
merged_data = merged_data.merge(redfin_clean, on="State", how="outer")

print(f"Merged data (first few rows):\n{merged_data.head()}")

def clean_sale_price(price):
    if isinstance(price, str):
        price = price.replace('$', '').replace(',', '')
        if 'K' in price:
            return float(price.replace('K', '').strip()) * 1000
        elif 'M' in price:
            return float(price.replace('M', '').strip()) * 1000000
        try:
            return float(price)
        except ValueError:
            return float('nan')
    return price

merged_data["2022 Median Sale Price"] = merged_data["2022 Median Sale Price"].apply(clean_sale_price)

merged_data["2022 MHI"] = pd.to_numeric(merged_data["2022 MHI"], errors="coerce")
merged_data["2022 Population"] = pd.to_numeric(merged_data["2022 Population"], errors="coerce")

merged_data["Price Per Capital"] = merged_data["2022 Median Sale Price"] / merged_data["2022 Population"]

merged_data["2022 Median Sale Price"].fillna(merged_data["2022 Median Sale Price"].mean(), inplace=True)
merged_data["2022 MHI"].fillna(merged_data["2022 MHI"].mean(), inplace=True)
merged_data["2022 Population"].fillna(merged_data["2022 Population"].mean(), inplace=True)

print(f"Final data before export:\n{merged_data.head()}")

merged_data.to_csv("Output.csv", index=False)

print("Final output.csv created with", len(merged_data), "rows.")
