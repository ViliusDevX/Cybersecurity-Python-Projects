# 📡 SSDP/UPnP Network Scanner (Python + Tkinter)

A simple Python GUI tool to **discover devices and services** on your local network using the **Simple Service Discovery Protocol (SSDP)**, part of **Universal Plug and Play (UPnP)**.  
The scanner sends a multicast `M-SEARCH` query and listens for responses from smart TVs, printers, NAS devices, consoles, routers, and other UPnP-enabled hardware.

---

## ✨ Features

- **Discover UPnP/SSDP devices** on your LAN (wired or wireless)
- **Tkinter-based GUI** — simple, portable, no extra dependencies
- Displays:
  - IP address
  - Service Type (ST)
  - Unique Service Name (USN)
  - Server software string
  - Device description URL (`LOCATION`)
- Adjustable scan timeout
- Multithreaded — responsive GUI during scans
- Automatic detection of your active network interface

---

## 📚 How It Works

This tool:

    Sends an SSDP multicast discovery packet:

    M-SEARCH * HTTP/1.1
    HOST: 239.255.255.250:1900
    MAN: "ssdp:discover"
    MX: 2
    ST: ssdp:all

    Waits for devices to respond with HTTP/1.1 200 OK headers describing themselves.

    Parses:

        ST (Service Type)

        USN (Unique Service Name)

        SERVER (software/OS info)

        LOCATION (URL to XML device description)

    Displays results in a sortable table.

## ⚖️ Legal & Ethical Use

    ✅ Allowed: Scanning your own network, home lab, or any environment where you have permission.

    ❌ Not allowed: Running on networks you do not control or without explicit consent — may violate laws or policies.
