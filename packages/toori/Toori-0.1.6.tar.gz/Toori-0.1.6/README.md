# Toori

Simple Python/C++ library for tunneling network traffic over http(s).

## Installation

```
pip install toori
```

## toori

Client module. Only available on Windows. 

Relies on [`WinDivert`](https://github.com/basil00/Divert) and [`Socket.IO`](https://socket.io/).

### Usage

```
toori -a <server address> -p 80 -f "tcp && tcp.DstPort == 443" -t polling
```

#### Note

The `toori` client requires Administrator privileges because of `WinDivert`.

## iro

Server module. 

Relies on [`Scapy`](https://scapy.net/) and [`Socket.IO`](https://socket.io/) via [`AIOHTTP`](https://github.com/aio-libs/aiohttp).

### Usage

#### HTTP

```
iro -p 80 -f "tcp and src port 443"
```

#### HTTPS

First retrieve Let's Encrypt certificates via [Certbot](https://certbot.eff.org/).

```
iro -p 443 -f "tcp and src port 443" -c <ssl cert path> -k <ssl key path>
```

### Running on Linux

Because the Linux kernel sends a `RST` to connections it did not establish, use the following command for Scapy to work:

```shell
sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s <local address> -j DROP
```

[See here](https://stackoverflow.com/questions/9058052/unwanted-rst-tcp-packet-with-scapy) for more information.
