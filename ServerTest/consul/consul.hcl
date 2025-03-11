data_dir = "E:\\ServerTest\\consul\\data"
client_addr = "0.0.0.0"
bind_addr = "192.168.2.35"
retry_join = ["192.168.2.26"]
log_level ="DEBUG"
ports {
  http = 8500
  serf_lan = 9301
  serf_wan = 9302
  server = 9300
}