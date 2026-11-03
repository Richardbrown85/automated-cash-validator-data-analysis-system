# Automated Cash Validator Data and Analysis System

## Overview

This project is a University Major Project focused on developing a software system that can communicate directly with cash validators, automatically capture testing data, organise it into structured test records, and prepare it for later analysis.

The initial prototype is being developed around an **NV9USB cash validator**.

The long-term aim is to reduce reliance on manual and spreadsheet-based test recording by creating a system that can capture validator events directly, link them to jobs and test sessions, record faults and notes, and eventually support analysis, dashboards, and possible AI/ML extensions.

## Project Aim

The project aims to:

- Establish reliable communication between a PC and an NV9USB cash validator.
- Capture real validator events automatically.
- Organise testing into jobs and individual test sessions.
- Record faults, issues, notes, and photographic evidence.
- Store captured information in a structured database.
- Prepare the data for analysis using Python and Pandas.
- Evaluate the prototype and identify future dashboard, comparison, and AI/ML extensions.

## Current Hardware Setup

- NV9USB cash validator
- IF17 interface
- 12V external power supply
- USB connection to the test laptop
- FTDI FT232R USB UART interface
- Windows USB Serial Port on **COM6**

The NV9 is currently being tested on an older laptop to keep the hardware-development setup separate from the main development machine.

## Communication Protocol

The NV9 communicates using **SSP (Smiley Secure Protocol)**.

Current serial settings:

- Baud rate: `9600`
- Data bits: `8`
- Parity: `None`
- Stop bits: `2`

Python communication is being handled using **PySerial**.

## Current Project Structure

```text
Automated_Cash_Validator_Data_Analysis_System/
│
├── src/
│   ├── nv9_connection_test.py
│   ├── nv9_sync.py
│   └── nv9_get_serial.py
│
├── requirements.txt
├── .gitignore
└── README.md