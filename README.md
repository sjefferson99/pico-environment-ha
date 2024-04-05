# Pico Environment control - HomeAssistant integration

## Introduction
This repository contains the files needed to add to a custom_component directory in Home Assistant to integrate with the [Pico Environment Control](https://github.com/sjefferson99/pico-environment-control) module.
It is currently in a beta, probably alpha how does this all work PoC state and is likely to be buggy, insecure, wrong and generally not great, but should work to some degree if carefully reviewed before installing in any production servers.

## Features
- Hub -> device -> entity structure
- Config flow to enable configuration entirely in the UI after installation
- Polling status of light and brightness
- On/Off control of the light
- Brightness control of the light
- Polling indoor humidity value

## Installation
As yet I have no desire to wrangle HA PRs or even investigate understanding HACS, so this is a straightforward copy the pico_environment folder to your custom_components folder.

Restart HomeAssistant and add the integration "Pico Environment". It will prompt for the hostname or IP address of the Pico and should automatically configure from there.

There is no encryption or any security at all at present, so this should be a local address safely behind a firewall.
