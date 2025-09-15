# OctoPrint-Fan2Mqtt

Publishes the current part-cooling fan speed to MQTT as a percentage `0–100` at the topic:
```
octoPrint/fan/speed
```
Values are derived from outgoing `M106/M107` G-code commands.

## Requirements
- OctoPrint ≥ 1.4
- **OctoPrint-MQTT** plugin installed, configured, and enabled
- An MQTT broker reachable by OctoPrint

## How it works
The plugin hooks into OctoPrint’s G-code queuing pipeline and detects:
- `M106 S0..255` → publishes a percentage = `round(S * 100 / 255)`
- `M106` → without parameter, it sets `100`
- `M107` → publishes `0`

Messages are **retained** by default so the last fan value is available to new subscribers.

> Limitation: this reflects what OctoPrint sends. If you print from the printer’s SD card or the firmware changes the fan on its own, the value cannot be read back.

## Installation
1. In OctoPrint go to **Settings → Plugin Manager → Get More... → ... from URL**  
2. Enter: 
    ```
    https://github.com/X4V1T0/OctoPrint-Fan2Mqtt/archive/refs/heads/main.zip
    ``` 
3. Install and restart OctoPrint.

## Configuration
No configuration is required. The MQTT topic is fixed to `octoPrint/fan/speed`.  
If you need a different topic or non-retained messages, edit the source and reinstall.

## Home Assistant example
Create an MQTT sensor:

```yaml
mqtt:
  sensor:
    - name: "Octoprint Fan Speed"
      state_topic: "octoPrint/fan/speed"
      unit_of_measurement: "%"
      icon: mdi:fan
