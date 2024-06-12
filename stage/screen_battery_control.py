import time
import os
import argparse
from mpu6050 import mpu6050

# Constantes pour la surveillance de la batterie
CAPACITE_BATTERIE_MAH = 10000
COURANT_MOYEN_ECRAN_ALLUME_MA = 1000
COURANT_MOYEN_ECRAN_ETEINT_MA = 500
SEUIL_BATTERIE_FAIBLE = 20
SEUIL_BATTERIE_CRITIQUE = 5
NIVEAU_LUMINOSITE_BASSE = 0.2

# Initialiser le capteur MPU6050
sensor = mpu6050(0x68)

# Analyser les arguments de la ligne de commande
parser = argparse.ArgumentParser(description="Contrôle de l'écran basé sur le mouvement du gyroscope et la surveillance de la batterie")
parser.add_argument("inactivity_threshold", type=int, help="Seuil de durée d'inactivité en secondes")
args = parser.parse_args()

seuil_inactivite = args.inactivity_threshold
heure_debut_inactivite = None

# Seuil de sensibilité au mouvement (ajuster en fonction des lectures de votre capteur)
seuil_mouvement = 0.5

# Fonction pour allumer les écrans
def allumer_les_ecrans():
    os.system("vcgencmd display_power 1")
    print("Écrans allumés")

# Fonction pour éteindre les écrans
def eteindre_les_ecrans():
    os.system("vcgencmd display_power 0")
    print("Écrans éteints")

# Fonction pour vérifier un mouvement significatif
def detecter_mouvement_significatif():
    donnees_accel = sensor.get_accel_data()
    x, y, z = donnees_accel['x'], donnees_accel['y'], donnees_accel['z']
    magnitude = (x**2 + y**2 + z**2)**0.5
    return magnitude > seuil_mouvement

# Fonction pour obtenir le temps de fonctionnement du système
def obtenir_uptime_systeme():
    with open('/proc/uptime', 'r') as f:
        uptime_secondes = float(f.readline().split()[0])
    return uptime_secondes

# Fonction pour calculer le pourcentage de batterie restant
def calculer_pourcentage_batterie_restant(uptime_secondes, capacite_batterie_mah, courant_moyen_ma):
    uptime_heures = uptime_secondes / 3600
    energie_utilisee_mah = uptime_heures * courant_moyen_ma
    batterie_restante_mah = capacite_batterie_mah - energie_utilisee_mah
    pourcentage_batterie_restant = (batterie_restante_mah / capacite_batterie_mah) * 100
    return max(0, min(100, pourcentage_batterie_restant))

# Fonction pour ajuster la luminosité de l'écran
def ajuster_luminosite(niveau):
    os.system(f"xrandr --output HDMI-1 --brightness {niveau}")

# Fonction pour éteindre le système
def eteindre_systeme():
    os.system("sudo shutdown -h now")

# Boucle principale pour surveiller le mouvement et contrôler les écrans
try:
    ecrans_allumes = True
    allumer_les_ecrans()

    while True:
        # Contrôle de l'écran basé sur le gyroscope
        if detecter_mouvement_significatif():
            heure_debut_inactivite = None
            if not ecrans_allumes:
                allumer_les_ecrans()
                ecrans_allumes = True
        else:
            if heure_debut_inactivite is None:
                heure_debut_inactivite = time.time()
            elif time.time() - heure_debut_inactivite > seuil_inactivite:
                if ecrans_allumes:
                    eteindre_les_ecrans()
                    ecrans_allumes = False

        # Déterminer la consommation de courant en fonction de l'état de l'écran
        if ecrans_allumes:
            courant_moyen_ma = COURANT_MOYEN_ECRAN_ALLUME_MA
        else:
            courant_moyen_ma = COURANT_MOYEN_ECRAN_ETEINT_MA

        # Surveillance de la batterie
        uptime_secondes = obtenir_uptime_systeme()
        pourcentage_batterie_restant = calculer_pourcentage_batterie_restant(
            uptime_secondes, CAPACITE_BATTERIE_MAH, courant_moyen_ma)
        
        print(f"Pourcentage de batterie restant: {pourcentage_batterie_restant:.2f}%")
        
        if pourcentage_batterie_restant < SEUIL_BATTERIE_CRITIQUE:
            print("Niveau de batterie critique atteint. Extinction du système.")
            eteindre_systeme()
        elif pourcentage_batterie_restant < SEUIL_BATTERIE_FAIBLE:
            print("Niveau de batterie faible. Réduction de la luminosité.")
            ajuster_luminosite(NIVEAU_LUMINOSITE_BASSE)
        
        time.sleep(30)  # Vérifier toutes les 30 secondes

except KeyboardInterrupt:
    allumer_les_ecrans()
    print("Sortie...")
