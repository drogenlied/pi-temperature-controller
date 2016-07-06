# Pi temperature controller
A Raspberry Pi based H-bridge controller designed to stabilize temperatures in an optics lab

## Hardware
  * Raspberry Pi (Model 2 recommended)
  * Measurement Specialities TSYS01 temperature sensor
  * Adum 14xx isolators between control and driver
  * VNH3SP30 H-bridge driver for output
  
## Features
  * Can control Peltier elements as well as resistive heaters for temperature stabilisation.
  * Fabrication should be possible in every university PCB shop
  * Hand soldering is possible but reflowing the VNH3SP30 is recommended
  
## Software
Test software is in this repository but https://github.com/Ulm-IQO/qudi is recommended for operation.
