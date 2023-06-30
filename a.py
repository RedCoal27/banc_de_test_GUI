import matplotlib.pyplot as plt
import time

# Créer un graphique vide
fig, ax = plt.subplots()
line, = ax.plot([], [])  # Ligne vide

# Définir les limites des axes
ax.set_xlim(0, 10)
ax.set_ylim(0, 1)

# Fonction pour mettre à jour les données du graphique
def update_graph(x_data, y_data):
    line.set_data(x_data, y_data)  # Mettre à jour les données de la ligne
    plt.draw()  # Réafficher le graphique

# Exemple de données
x = []
y = []

# Mettre à jour le graphique avec de nouvelles données toutes les 2 secondes
while True:
    x.append(len(x))
    y.append(len(x)/10)
    update_graph(x, y)
    plt.pause(2)  # Faire une pause de 2 secondes
