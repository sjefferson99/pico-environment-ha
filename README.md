# Pico Environment control - HomeAssistant integration

## Introduction
This repository contains the files needed to add to a custom_component directory in Home Assistant to integrate with the [Pico Environment Control](https://github.com/sjefferson99/pico-environment-control) module.
It is currently in a beta, probably alpha how does this all work PoC state and is likely to be buggy, insecure, wrong and generally not great, but should work to some degree if carefully reviewed before installing in any production servers.

## Features
- On/Off control of the light

## Installation
As yet I have no desire to wrangle HA PRs or even investigate understanding HACS, so this is a straightforward copy the pico_environment folder to your custom_components folder and use the configuration.yaml in the repo root as a guide to manually configuring your HA to use the custom module.

Update the name to your preferred value and the ip_address to where the pico can be found on the network. There is no encryption or any security at all at present, so this should be a local address safely behind a firewall.

