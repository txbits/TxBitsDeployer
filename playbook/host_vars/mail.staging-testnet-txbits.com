open_tcp_ports:
  - port: smtp
    allowed: 0.0.0.0/0
  - port: ssmtp
    allowed: 0.0.0.0/0
  - port: imaps
    allowed: 0.0.0.0/0
  - port: imap2
    allowed: 0.0.0.0/0
