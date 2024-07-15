import time
import os
import argparse
from mpu6050 import mpu6050

# Initialiser le capteur MPU6050
sensor = mpu6050(0x68)

# Analyser les arguments de la ligne de commande
parser = argparse.ArgumentParser(description="Contrôle de l'écran basé sur le mouvement du gyroscope")
parser.add_argument("inactivity_threshold", type=int, help="Seuil de durée d'inactivité en secondes")
args = parser.parse_args()

seuil_inactivite = args.inactivity_threshold
heure_debut_inactivite = None

# Seuil de sensibilité au mouvement (ajuster en fonction des lectures de votre capteur)
seuil_mouvement = 40

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
    donnees_accel = sensor.get_gyro_data()
    x, y, z = donnees_accel['x'], donnees_accel['y'], donnees_accel['z']
    magnitude = (x**2 + y**2 + z**2)**0.5
    print("\n", magnitude)
    return magnitude > seuil_mouvement

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

        time.sleep(2)  # Vérifier toutes les 2 secondes

except KeyboardInterrupt:
    allumer_les_ecrans()
    print("Sortie...")

