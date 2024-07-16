import RPi.GPIO as GPIO
import time
import os
import threading
import subprocess

BOUTON_PIN = 17  # Broche GPIO connectée au bouton
SEUIL_APPUI = 1  # Seuil de temps pour distinguer l'appui long
DETECTION_TEMPS = 0.01  # Intervalle de temps pour détecter l'état du bouton
pairing_thread = None
pairing_in_progress = False

def configuration():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BOUTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BOUTON_PIN, GPIO.FALLING, callback=callback_bouton, bouncetime=300)

def callback_bouton(channel):
    global pairing_in_progress
    heure_debut = time.time()

    # Attendre que le bouton soit relâché
    while GPIO.input(BOUTON_PIN) == GPIO.LOW:
        time.sleep(DETECTION_TEMPS)

    temps_appui = time.time() - heure_debut

    if temps_appui >= SEUIL_APPUI:
        if pairing_in_progress:
            # Si l'appairage est en cours, interrompre et éteindre
            print("Interrompre l'appairage Bluetooth et éteindre")
        gerer_appui_long()
    else:
        gerer_appui_court()

def gerer_appui_court():
    global pairing_thread, pairing_in_progress
    print("Appui court détecté")
    pairing_in_progress = True
    # Utiliser un thread pour le processus d'appairage Bluetooth
    pairing_thread = threading.Thread(target=demarrer_pairing)
    pairing_thread.start()
	
def demarrer_pairing():
    global pairing_in_progress
    try:
        subprocess.call(["python3", "/home/pi/pair_device_dbus.py"])
    finally:
        pairing_in_progress = False

def stop_pairing():
    global pairing_thread, pairing_in_progress
    # Cette méthode dépend de la manière dont vous pouvez interrompre le processus d'appairage.
    # Si le processus d'appairage est en cours, essayez de l'arrêter ici.
    if pairing_thread is not None:
        # Si possible, arrêter le thread d'appairage ici
        pairing_thread.join()
    pairing_in_progress = False

def gerer_appui_long():
    print("Appui long détecté")
    # Implémenter la logique d'arrêt ici
#    os.system("sudo shutdown -h now")

def main():
    configuration()
    try:
        print("Écoute des appuis sur le bouton...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Sortie du programme...")

if __name__ == "__main__":
    main()
