# Pingline - a less cool version of [gping](https://github.com/orf/gping)

This is just a package for me to practice working with PyPi. You should probably use [gping](https://github.com/orf/gping) instead. It doesn't require a heavy `matplotlib` dependency.

## Why even use this?

This is helpful for debugging ping problems with your WiFi:
* Try starting the interactive plotter and launching [fast.com](https://fast.com) - see the impact of heavy traffic on your ping
* Check if the router ping is as bad as internet ping. If so, the problem is with your router, else it's probably your ISP

## Installation

```
pip install pingline
```

## Usage

Launch the recorder - it's pinging our hosts and dumping the ping time-series into a log file, by default `ping_log.csv`. This CSV plays nicely with Excel, if you want to explore the data manually.
```
pingline recorder --interval=0 --router-host=192.168.0.1 --internet-host=google.com
```

Launch the interactive plotter - it watches the log file and shows a live graph of ping data.
```
pingline plotter --interactive --last-n-minutes=5
```
https://user-images.githubusercontent.com/4249837/177884337-d6c235b1-d017-4c9e-97c2-8a38d601e28c.mp4
