Raspberry Pi Zero 2 w Setup 
Sac à main 

* connect as : pi
  password : 123

* Pour envoyer les images il faut ajouter "_APPID" à la fin du nom de l'image. Peut être changer dans le fichier watch_for_images.sh variable APP_IDENFIER

* Pour ajouter un wifi il faut d'abord brancher la carte SD à l'ordinateur, puis modifier le fichier wpa_supplicant.conf 

* Cablage :     VCC -> 3.3V      SCL -> SCL	SDA -> SDA	GND -> GROUND		i2cdetect -y 1 dans le terminal pour voir si le composant est bien connecté 
		bouton : VCC -> 3.3V	GND -> GROUND	S -> GPIO 17

* Avant le premier allumage, il faut effacer le fichier last_feh_command.sh pour que le logo s'affiche et non pas le dernier image envoyé

* .bash -> .sh 

* Tutoriel en ligne "dupliquer carte SD raspberry pi", j'ai utilisé Win32DiskImager

---------------------------------------------------------------------------------------------------------------------------------------------------------------

button.py :	Lance l'appairage bluetooth si bouton appuyé (code ne se lance pas encore au démarrage, faut créer fichier systemd)
button3.py :	Lance l'appairage bluetooth si bouton appuyé, eteint le raspberry pi si reste appuyé pendant plus de 2sec (modifiable, vairable SEUIL_APPUI)
screens.py : 	BESOIN D'UN ENVINRONMENT VIRTUEL ($ source /home/pi/myenv/bin/activate pour l'activer) Eteint les écrans si l'accéléromètre ne bouge pas après un temps donné à l'exécution, allume les écrans dès qu'il bouge (code ne se lance pas encore au démarrage, faut créer fichier systemd)
battery.py : 	Affiche le niveau et le voltage de la batterie dans le terminal (code ne se lance pas encore au démarrage, faut créer fichier systemd)
pair_device_dbus.py : 	L'appairage bluetooth pour un temps donné (modifiable dans le fichier) 
temperature_monitor.py : 	Surveille la témperature du CPU, si dépasse 80° le raspberry va s'eteindre (code ne se lance pas encore au démarrage, faut créer fichier systemd)
watch_for_images.sh :	Affiche l'image envoyé, efface l'image qui se termine pas avec _APPID
startup_display_last_image.sh :	Au démarrage du raspberry, affiche le dernier image envoye, ou le logo si le dernier image envoyé n'existe pas 
.service :	Fichiers systemd dans le dossier /etc/systemd/system/ pour que le fichier donné s'exécute lorsque le raspberry demarre 
rpi_cablage.jpg, rpi_cablage.jpg

--------------------------------------------------- INCOMPLETE, MIEUX DE DUPLIQUER LA CARTE SD ----------------------------------------------------------------

1. Installer Raspberry Pi OS 64-bits (tutoriels youtubes) 

2. Changer la taille RAM 
    sudo nano /etc/dphys-swapfile
		CONF_SWAPSIZE=100	=>	CONF_SWAPSIZE=2048
    sudo reboot
	
	#si probleme bizzare où résolution très petite 
	sudo nano /boot/firmware/cmdline.txt
		video=HDMI-A-1:1920x1080M@60D #ajouter au debut de la ligne 
	
3. Mises-à-jours et packages
   sudo apt-get update
   sudo apt-get upgrade
   apt install bluez-obexd
   apt-get install feh
   apt-get install inotify-tools
   sudo apt remove python3-rpi.gpio
   sudo apt install python3-rpi-lgpio
   
4. Recevoir des images
    sudo nano /etc/dbus-1/system.d/bluetooth.conf
		<!DOCTYPE busconfig PUBLIC "-//freedesktop//DTD D-BUS Bus Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/dbus/1.0/busconfig.dtd">
<busconfig>

  <!-- ../system.conf have denied everything, so we just punch some holes -->

  <policy user="root">
    <allow own="org.bluez"/>
    <allow send_destination="org.bluez"/>
    <allow send_interface="org.bluez.AdvertisementMonitor1"/>
    <allow send_interface="org.bluez.Agent1"/>
    <allow send_interface="org.bluez.MediaEndpoint1"/>
    <allow send_interface="org.bluez.MediaPlayer1"/>
    <allow send_interface="org.bluez.Profile1"/>
    <allow send_interface="org.bluez.GattCharacteristic1"/>
    <allow send_interface="org.bluez.GattDescriptor1"/>
    <allow send_interface="org.bluez.LEAdvertisement1"/>
    <allow send_interface="org.freedesktop.DBus.ObjectManager"/>
    <allow send_interface="org.freedesktop.DBus.Properties"/>
    <allow send_interface="org.mpris.MediaPlayer2.Player"/>
    <allow own="org.bluez.obex"/>
    <allow send_destination="org.bluez.obex"/>
    <allow send_interface="org.bluez.obex.Client1"/>
    <allow send_interface="org.bluez.obex.Session1"/>
    <allow send_interface="org.bluez.obex.Transfer1"/>
    <allow send_interface="org.bluez.obex.ObjectPush1"/> 
  </policy>

  <policy user="pi">
    <allow own="org.bluez.obex"/>
    <allow send_destination="org.bluez.obex"/>
    <allow send_interface="org.bluez.obex.Client1"/>
    <allow send_interface="org.bluez.obex.Session1"/>
    <allow send_interface="org.bluez.obex.Transfer1"/>
    <allow send_interface="org.bluez.obex.ObjectPush1"/> 
  </policy>

  <!-- Allow users of the bluetooth group to communicate -->
  <policy group="bluetooth">
    <allow send_destination="org.bluez"/>
  </policy>

  <policy context="default">
    <allow send_destination="org.bluez"/>
  </policy>

</busconfig>


    sudo nano /etc/systemd/system/obexd.service
		[Unit]
		Description=OBEX Daemon for Bluetooth file transfers
		After=bluetooth.service
		Requires=bluetooth.service

		[Service]
		User=pi
		Group=pi
		Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket
		ExecStart=/usr/libexec/bluetooth/obexd -n -a -r /home/pi/Pictures
		Restart=always

		[Install]
		WantedBy=multi-user.target
	sudo systemctl daemon-reload
	sudo systemctl enable obexd.service
	sudo systemctl start obexd.service
	sudo systemctl status obexd.service
	
5. Surveiller un dossier
    nano watch_for_images.sh
FICHIER DANS CE HUB

	sudo nano /etc/systemd/system/watch_for_images.service
		FICHIER DANS CE HUB
		
	sudo systemctl daemon-reload
	sudo systemctl enable watch_for_images.service
	sudo systemctl start watch_for_images.service

	sudo systemctl status watch_for_images.service
	
6.  Logo/dernier image affiché (faut effacer last_feh_command.sh pour la première demarrage)
	nano startup_display_last_image.sh
FICHIER DANS CE HUB

	cp -r /etc/xdg/lxsession ~/.config/
	echo "@/home/pi/startup_display_last_image.sh" >> /home/pi/.config/lxsession/LXDE-pi/autostart
	
7.	Splash screen 
	sudo nano /boot/firmware/config.txt
		disable_splash=1
		
	sudo nano /boot/firmware/cmdline.txt
		console=serial0,115200 console=tty3 root=PARTUUID=d6226580-02 rootfstype=ext4 fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles loglevel=0 vt.global_cursor_default=0

	sudo nano /etc/lightdm/lightdm.conf
		[Seat:*]
		xserver-command=X -nocursor

	
	sudo mkdir /usr/share/plymouth/themes/mytheme
	sudo cp /path/to/your/image.png /usr/share/plymouth/themes/mytheme/splash.png
	sudo nano /usr/share/plymouth/themes/mytheme/mytheme.plymouth
		[Plymouth Theme]
		Name=MyTheme
		Description=Custom splash screen
		ModuleName=script

		[script]
		ImageDir=/usr/share/plymouth/themes/mytheme
		ScriptFile=/usr/share/plymouth/themes/mytheme/mytheme.script
		
	sudo nano /usr/share/plymouth/themes/mytheme/mytheme.script
		wallpaper_image = Image("splash.png");
		screen_width = Window.GetWidth();
		screen_height = Window.GetHeight();
		resized_image = wallpaper_image.Scale(screen_width, screen_height);
		wallpaper_sprite = Sprite(resized_image);
		wallpaper_sprite.SetZ(-100);
		
	sudo plymouth-set-default-theme -R mytheme
	
8. Eteindre/Allumer les écrans 
	sudo nano /boot/firmware/config.txt
		dtoverlay=vc4-kms-v3d	=>	dtoverlay=vc4-fkms-v3d
	sudo reboot
	vcgencmd display_power 0 #éteindre l'écran
	vcgencmd display_power 1 #allumer l'écran
	
9. L'écran ne s'endort pas 
	sudo apt-get install xscreensaver
	après faut le desactivé 
	
10. Cacher le panel
clique droite sur le panel -> panel settings -> notifications off 
							   -> panel settings -> hide panel -> 0 pxl 

---------------------------------------------------------------------------------------------------------------------------------------------------------------

							
