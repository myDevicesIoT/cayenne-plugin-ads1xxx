# Cayenne ADS1XXX Plugin
A plugin allowing the [Cayenne Pi Agent](https://github.com/myDevicesIoT/Cayenne-Agent) to read data from ADS1XXX devices (ADS1014, ADS1015, ADS1114, ADS1115) and display it in the [Cayenne Dashboard](https://cayenne.mydevices.com).

## Requirements
### Hardware
* [Rasberry Pi](https://www.raspberrypi.org).
* An ADS1XXX extension, e.g. [ADS1115](https://www.adafruit.com/product/1085).

### Software
* [Cayenne Pi Agent](https://github.com/myDevicesIoT/Cayenne-Agent). This can be installed from the [Cayenne Dashboard](https://cayenne.mydevices.com).
* [Git](https://git-scm.com/).

## Getting Started

### 1. Installation

   From the command line run the following commands to install this plugin.
   ```
   cd /etc/myDevices/plugins
   sudo git clone https://github.com/myDevicesIoT/cayenne-plugin-ads1xxx.git
   ```

### 2. Setting the device class

   Specify the device you are using by setting the `class` value under the `ADS` section in the `cayenne_ads1xxx.plugin` file.
   By default this is set to `ADS1115` but it can be set to use any of the classes in the `cayenne_ads1xxx` module. If your 
   device has fewer channels than the `ADS1115` or you do not want the raw channel values to be displayed in the Cayenne 
   dashboard you can disable any of the individual input sections in `cayenne_ads1xxx.plugin`.

### 3. Restarting the agent

   Restart the agent so it can load the plugin.
   ```
   sudo service myDevices restart
   ```
   Temporary widgets for the plugin should now show up in the [Cayenne Dashboard](https://cayenne.mydevices.com). You can make them permanent by clicking the plus sign.

   NOTE: If the temporary widgets do not show up try refreshing the [Cayenne Dashboard](https://cayenne.mydevices.com) or restarting the agent again using `sudo service myDevices restart`.