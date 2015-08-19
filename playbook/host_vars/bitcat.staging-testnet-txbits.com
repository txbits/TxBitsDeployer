open_tcp_ports:
  - port: "{{port.bitcoind_pipe}}"
    allowed: "{{hosts.limecat}}"
