open_tcp_ports:
  - port: "{{port.litecoind_pipe}}"
    allowed: "{{hosts.limecat}}"
