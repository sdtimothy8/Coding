$.post('/vmmanager/creator/',{"vm_iso_path":"/home/vagary/Downloads/cent7.iso"},"JSON")
$.post('/vmmanager/vm/',{"vm_name":"hello","vm_iso_path":"/home/vagary/Downloads/cent7.iso","vm_install_method":1,"vm_cpu":1,"vm_mem":1024,"vm_size":10},"JSON")


$.post('/vmmanager/lifecycle/',{"vm_list":["cent","hello"],"vm_status":"startup"},"JSON")
$.post('/vmmanager/lifecycle/',{"vm_list":["cent","hello"],"vm_status":"shutdown"},"JSON")

$.post('/vmmanager/remove/',{"vm_list":["hello"]},"JSON")