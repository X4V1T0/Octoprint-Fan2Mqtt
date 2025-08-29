import re
import octoprint.plugin

class Fan2Mqtt(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
):
    def __init__(self):
        self.mqtt_publish = None

    def on_after_startup(self):
        self._logger.info("Fan2MQTT iniciado")
        helpers = self._plugin_manager.get_helpers("mqtt", "mqtt_publish")
        if helpers and helpers.get("mqtt_publish"):
            self.mqtt_publish = helpers["mqtt_publish"]
            self._logger.info("Helper MQTT conectado")
        else:
            self._logger.error("Helper MQTT NO disponible. ¿OctoPrint-MQTT habilitado?")

    # Soporta firmas antiguas y nuevas del hook: con o sin 'gcode'
    def hook_gcode_queuing(self, *args, **kwargs):
        """
        Firmas posibles:
        (comm, phase, cmd, cmd_type, gcode, *rest)   # nuevas
        (comm, phase, cmd, cmd_type, *rest)          # antiguas
        """
        try:
            if len(args) >= 5:
                comm, phase, cmd, cmd_type, gcode = args[:5]
            elif len(args) >= 4:
                comm, phase, cmd, cmd_type = args[:4]
                # Derivar gcode si es posible
                m = re.match(r"\s*([GMT]\d+)", cmd or "", re.IGNORECASE)
                gcode = m.group(1).upper() if m else None
            else:
                # No hay suficientes argumentos, no hacemos nada
                return None

            if gcode == "M106":
                m = re.search(r"\bS(\d+)\b", cmd or "", re.IGNORECASE)
                s = int(m.group(1)) if m else 255
                s = max(0, min(255, s))
                pct = int(round(s * 100.0 / 255.0))
                if self.mqtt_publish:
                    self.mqtt_publish("octoPrint/fan/speed", str(pct), retained=True)
                    self._logger.info("M106 -> %s%% publicado", pct)
                else:
                    self._logger.warning("M106 -> %s%% pero sin helper MQTT", pct)

            elif gcode == "M107":
                if self.mqtt_publish:
                    self.mqtt_publish("octoPrint/fan/speed", "0", retained=True)
                    self._logger.info("M107 -> 0%% publicado")
                else:
                    self._logger.warning("M107 -> 0%% pero sin helper MQTT")

        except Exception as e:
            self._logger.exception("Error en Fan2MQTT: %s", e)

        return None

__plugin_name__ = "Fan2MQTT"
__plugin_version__ = "0.0.3"
__plugin_pythoncompat__ = ">=3,<4"

# Instancia del plugin
__plugin_implementation__ = Fan2Mqtt()

# Registra el MÉTODO DE INSTANCIA, no la función de clase
__plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.queuing": (__plugin_implementation__.hook_gcode_queuing, 100)
}