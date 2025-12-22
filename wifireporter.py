import subprocess
import requests
import base64
import time

#TOPScience IPstore google apps script
gas_url="https://script.google.com/macros/s/AKfycbxCk4RMYfEdMGHp7H65H8zFglMbjSVh_K85MhWRkZKUAAjtlzGLsurvVKCByIAwp6ul5w/exec"
gas_id="kgreenhouse"

def report_ip():
  ss = subprocess.check_output(["iwlist", "wlan0", "scan"],text=True).split('\n')
  lines = [s.strip() for s in ss]
  #cari yang berawalan 'ESSID:'
  ssid = ""
  for l in lines:
    if l.find('ESSID:') >= 0:
      ssid=l.split(':')[1]
      #hasilnya masih ada tanda ""
      ssid = ssid.split('"')[1]
      break

  if ssid != "":
    print("Sedang terhubung ke SSID:", ssid)
    ipadr = subprocess.check_output(["hostname", "-I"],text=True).strip()
    print("IP address:",ipadr)
    #kirim ke GAS
    #convert dulu jadi base64
    ipb64 = base64.b64encode(ipadr.encode('ascii')).decode('ascii')
    #cek apa ngrok terhubung
    R = requests.get("http://localhost:4040/api/tunnels")
    ngrok_url=""
    if R.ok:
      rj = R.json()
      ngrok_url=rj["tunnels"][0]["public_url"]
      ng_b64=base64.b64encode(ngrok_url.encode('ascii')).decode('ascii')
    complete_url = gas_url + "?ip=" + ipadr + "&id=" + gas_id + "&s=" + ssid + "&d=" + ngrok_url
    print("Requesting:")
    print(complete_url)
    R=requests.get(complete_url)
    if R.ok:
      print(R.status_code)
      print(R.text)
  else:
    print("Tidak bisa menemukan SSID yang sedang terhubung")

while True:
  report_ip()
  time.sleep(600) #10 menit sekali


