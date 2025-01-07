import socket
import argparse
from colorama import init, Fore
import re

init(autoreset=True)

def get_service_version(s, port):
	try:
		s.settimeout(2)  
		if port == 80 or port == 443:
			s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
		elif port == 21:
			pass  
		elif port == 25:
			s.send(b"HELO test\r\n")
		else:
			
			s.send(b"\r\n")
		
		banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
		version_match = re.search(r'(\d+\.[\d\.]+)', banner)
		if version_match:
			return f"{banner}\nVersiyon: {version_match.group(1)}"
		return banner
	except socket.timeout:
		return (Fore.RED + "Timeout Error: Banner alınamadı")
	except Exception as e:
		return (Fore.RED + f"Hata: {str(e)}")

def scan(adress, end_port, timeout):
	print(Fore.GREEN + f"\nPortlar taranıyor: {adress}\n")
	open_port_number = 0
	
	for port in range(1,(int(end_port) + 1)):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(float(timeout))
			
			isConnected = s.connect_ex((adress,port))
			if isConnected == 0:
				try:
					service = socket.getservbyport(port)
				except OSError:
					service = "bilinmeyen servis"
				
				version_info = get_service_version(s, port)
				
				print(Fore.WHITE + "-------------------------")
				print(Fore.GREEN + f"Port {port} açık")
				print(Fore.YELLOW + f"Servis: {service}")
				print(Fore.CYAN + f"Banner/Versiyon Bilgisi: {version_info}")
				open_port_number += 1
				
		except Exception as e:
			print(Fore.RED + f"Port {port} taranırken hata: {str(e)}")
		finally:
			s.close()
	
	print(Fore.WHITE + "-------------------------\n")
	print(Fore.RED + f"{open_port_number} adet açık port bulundu: {adress}\n")

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--adress', help='Specify the address', required=True)
parser.add_argument('--end-port',help="The port at which the port scan will end",required=False,default=100)
parser.add_argument('-t','--timeout',help="Timeout count",required=False,default=1.0)
args = parser.parse_args()


if __name__ == "__main__":
	scan(args.adress,args.end_port,args.timeout)
