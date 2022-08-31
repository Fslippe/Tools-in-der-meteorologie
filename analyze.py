import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import scipy.stats as stats
import matplotlib.dates as mdates
import matplotlib.ticker as plticker
plt.rcParams.update({'font.size': 22})

def height_adjust():
    """
    Heigh adjustment of data imported from QGIS Read file and export
    file name has to be changed when adjusting different datasets
    """
    z0 = 277
    dT = 6.5 #per km

    data = pd.read_csv("export/height_data_2.csv") #READ FILE
    #data = pd.read_csv("export/height_data.csv")

    data["T_adjusted"] = data["Absolute_temperature_degC"] - (z0 - data["GPS_Altitude"])*dT/1000
    data["T_diff_adjusted"] = data["Temperature_diff_K"] - (data["Absolute_temperature_degC"] - data["T_adjusted"])
    data.index = data["Time_UTC"]
    data["T_adjusted"].plot(label="T_adjusted")
    data["Absolute_temperature_degC"].plot(label="Absolute_temperature_degC")

    #data.to_csv("export/data_adjusted_2.csv") #EXPORT FILE
    #data.to_csv("export/data_adjusted.csv")

    plt.title("Comparison between altitude adjusted temperat|ure and absolute temperature")
    plt.legend()
    plt.ylabel("Temperature ($^\circ C$)")
    plt.show()
    slope, intercept, r_value, pv, se = stats.linregress(data["GPS_Altitude"].to_numpy(), data["Absolute_temperature_degC"].to_numpy())
    plt.title("Linear regression Temperature against Altitude\n$R^2 = $ %.2f, $P = $ %.4f" %(r_value**2, pv))
    sns.regplot(data["GPS_Altitude"], data["Absolute_temperature_degC"], scatter=True)
    sns.regplot(data["GPS_Altitude"], data["Absolute_temperature_degC"], scatter=False, color="r", label="$y=$%.4f$x$ + %.2f" %(slope, intercept))
    plt.legend()
    plt.show()

data = pd.read_csv("export/data_adjusted_tree.csv")
data2 = pd.read_csv("export/data_adjusted_tree_2.csv")
mask = ~np.isnan(data["lc_bldn"])
mask2 = ~np.isnan(data2["lc_bldn"])
data_full = data.append(data2)
mask_full = ~np.isnan(data_full["lc_bldn"])

def lc_regplot(lc, df, mask):
    slope, intercept, r_value, pv, se = stats.linregress(df[lc].to_numpy()[mask]*100, df["T_diff_adjusted"].to_numpy()[mask])
    plt.title("Linear regression altitude adjusted temperature against Land Cover\n$R^2 = $ %.2f, $P = $ %.4f" %(r_value**2, pv))
    sns.regplot(y = df["T_diff_adjusted"].to_numpy()[mask], x = df[lc].to_numpy()[mask]*100, scatter=True)
    sns.regplot(y = df["T_diff_adjusted"].to_numpy()[mask], x = df[lc].to_numpy()[mask]*100, scatter=False, color="r",  label="$y=$%.3f$x$ + %.2f" %(slope, intercept))
    plt.xlabel(lc)
    plt.ylabel("Temperature difference ($^\circ$C)")
    plt.legend()
    plt.show()

def reg(percentage):
    df = data_full[data_full["lc_bldn"] > percentage]
    df["green"] = df["lc_tree"] + df["lc_grss"]
    mask_df = ~np.isnan(df["lc_bldn"])
    df[mask_df].to_csv("data_bldn40.csv")
    print(np.max(df["GPS_Altitude"].to_numpy()))
    print(np.min(df["GPS_Altitude"].to_numpy()))

def reg(percentage):
    df = data_full[data_full["lc_bldn"] > percentage]
    df["green"] = df["lc_tree"] + df["lc_grss"]
    mask_df = ~np.isnan(df["lc_bldn"])
    df[mask_df].to_csv("data_bldn40.csv")
    print("Max height", np.max(df["GPS_Altitude"].to_numpy()))
    print("Min height", np.min(df["GPS_Altitude"].to_numpy()))
    lc_regplot("green", df, mask_df)
    lc_regplot("lc_bldn", df, mask_df)
    lc_regplot("lc_pavd", df, mask_df)
    lc_regplot("lc_grss", df, mask_df)
    lc_regplot("lc_tree", df, mask_df)
    lc_regplot("lc_watr", df, mask_df)

def main():
    height_adjust()
    lc_regplot("lc_bldn", data_full, mask_full)
    lc_regplot("lc_pavd", data_full, mask_full)
    lc_regplot("lc_grss", data_full, mask_full)
    lc_regplot("lc_tree", data_full, mask_full)
    lc_regplot("lc_watr", data_full, mask_full)
    reg(0.4)

if __name__ == "__main__":
    main()
