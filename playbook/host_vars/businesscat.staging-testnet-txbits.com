open_tcp_ports:
  - port: "{{port.postgresql}}"
    allowed: "{{hosts.limecat}}"
  - port: "{{port.postgresql}}"
    allowed: "{{hosts.longcat}}"
  - port: "{{port.memcached_pipe}}"
    allowed: "{{hosts.longcat}}"
