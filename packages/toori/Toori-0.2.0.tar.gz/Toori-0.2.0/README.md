# ![icon](https://github.com/kokseen1/Toori/blob/master/toori/icon.png?raw=true) Toori 

Simple Python/C++ library for tunneling network traffic over http(s).

## Prerequisites

- [MSVC](https://visualstudio.microsoft.com/vs/features/cplusplus/)

- pybind11

```
pip install pybind11
```

## Installation

```
pip install toori
```

## Usage

### toori

Client module. Requires Administrator privileges.

```
toori -a <server address> -p 80 -f "tcp && tcp.DstPort == 443" -t polling
```

Graphical interface

```
toori -g
```

### iro

Server module.

#### HTTP

```
iro -p 80 -f "tcp and src port 443"
```

#### HTTPS

First retrieve Let's Encrypt certificates via [Certbot](https://certbot.eff.org/).

```
iro -p 443 -f "tcp and src port 443" -c <ssl cert path> -k <ssl key path>
```

#### Running on Linux

Because the Linux kernel sends a `RST` to connections it did not establish, use the following command for Scapy to work:

```shell
sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s <local address> -j DROP
```

[See here](https://stackoverflow.com/questions/9058052/unwanted-rst-tcp-packet-with-scapy) for more information.
