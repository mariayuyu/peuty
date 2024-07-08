import os
import time
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

BUS_NAME = "org.bluez"
AGENT_INTERFACE = "org.bluez.Agent1"
ADAPTER_INTERFACE = "org.bluez.Adapter1"
AGENT_PATH = "/test/agent"
CAPABILITY = "NoInputNoOutput"

class PairingAgent(dbus.service.Object):
    def __init__(self, bus, path):
        dbus.service.Object.__init__(self, bus, path)


    @dbus.service.method(AGENT_INTERFACE, in_signature="os", out_signature="")
    def AuthorizeService(self, device, uuid):
        print(f"AuthorizeService ({device}, {uuid})")
        return

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="")
    def RequestAuthorization(self, device):
        print(f"RequestAuthorization ({device})")
        return

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        print(f"RequestPinCode ({device})")
        return "0000"

    @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
    def DisplayPinCode(self, device, pincode):
        print(f"DisplayPinCode ({device}, {pincode})")

    @dbus.service.method(AGENT_INTERFACE, in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        print(f"RequestPasskey ({device})")
        return dbus.UInt32(123456)

    @dbus.service.method(AGENT_INTERFACE, in_signature="ouq", out_signature="")
    def DisplayPasskey(self, device, passkey, entered):
        print(f"DisplayPasskey ({device}, {passkey}, {entered})")

    @dbus.service.method(AGENT_INTERFACE, in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        print(f"RequestConfirmation ({device}, {passkey})")
        return  # Automatically confirm the pairing

    @dbus.service.method(AGENT_INTERFACE, in_signature="", out_signature="")
    def Release(self):
        print("Release")
        return


def make_discoverable(duration=60):
    bus = dbus.SystemBus()
    adapter = dbus.Interface(bus.get_object(BUS_NAME, "/org/bluez/hci0"), "org.freedesktop.DBus.Properties")
    adapter.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(1))
    print(f"Device is discoverable for {duration} seconds")
    time.sleep(duration)
    adapter.Set("org.bluez.Adapter1", "Discoverable", dbus.Boolean(0))
    print("Device is no longer discoverable")

def device_added_callback(object_path, interfaces):
    if "org.bluez.Device1" in interfaces:
        device_properties = interfaces["org.bluez.Device1"]
        if device_properties.get("Paired", False):
            print(f"Device paired: {object_path}")
            os.system("/home/pi/display_image.sh")

def handle_pairing():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    agent = PairingAgent(bus, AGENT_PATH)
    manager = dbus.Interface(bus.get_object(BUS_NAME, "/org/bluez"), "org.bluez.AgentManager1")
    manager.RegisterAgent(AGENT_PATH, CAPABILITY)
    print("Agent registered")

    make_discoverable(60)

    manager.RequestDefaultAgent(AGENT_PATH)
    print("Agent set as default")

    # Add a signal receiver to handle successful pairing
    bus.add_signal_receiver(device_added_callback, bus_name="org.bluez", signal_name="InterfacesAdded")

    GLib.MainLoop().run()

if __name__ == "__main__":
    handle_pairing()
