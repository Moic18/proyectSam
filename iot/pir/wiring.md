# PIR Sensor Wiring (HC-SR501)

| PIR Pin | ESP32-CAM Pin | Notes |
|---------|---------------|-------|
| VCC     | 5V            | Power supply (use 5V from regulator) |
| GND     | GND           | Common ground |
| OUT     | GPIO13        | Connect through jumper wire |

## Tips

- Adjust the **sensitivity** potentiometer to reduce false positives.
- Set the **delay** potentiometer to the minimum value so the backend receives events quickly.
- Use shielded cables if you experience noise, and keep the PIR away from heat sources.
