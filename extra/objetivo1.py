import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dataset.csv")

conducta_nucleo = df.groupby("NUCLEO_FAMILIAR")["CONDUCTA_INAPROPIADA"]
conducta_zona = df.groupby("ZONA")["CONDUCTA_INAPROPIADA"]

conducta_nucleo_stats = pd.DataFrame({
    "Recuento": conducta_nucleo.count(),
    "Media": conducta_nucleo.mean(),
}).sort_values("Media")

conducta_zona_stats = pd.DataFrame({
    "Recuento": conducta_zona.count(),
    "Media": conducta_zona.mean(),
}).sort_values("Media")

# ---- Grafico Conducta-Nucleo ---- #
conducta_nucleo_stats.plot(kind="bar", y=["Media"])
plt.xticks(rotation=0) 
plt.title("Estadísticas de Conducta Inapropiada por Núcleo Familiar")
plt.xlabel("Núcleo Familiar")
plt.ylabel("Valor")
plt.show()
# --------------------------------- #

# ---- Grafico Conducta-Zona ---- #
conducta_zona_stats.plot(kind="bar", y=["Media"])
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.35) 
plt.title("Estadísticas de Conducta Inapropiada por Zona de Vivienda")
plt.xlabel("Zona")
plt.ylabel("Valor")
plt.show()
# --------------------------------- #