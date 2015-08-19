open_tcp_ports:
  - port: http
    allowed: 0.0.0.0/0
  - port: https
    allowed: 0.0.0.0/0
