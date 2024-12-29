import socket
import argparse
from colorama import init , Fore

init(autoreset=True)

def scan(adress,end_port=100,timeout=1):
	print(Fore.GREEN + f"\nScannin ports at {adress}\n")
	open_port_number = 0
	for port in range(1,(int(end_port) + 1)):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.settimeout(int(timeout))

		isConnected = s.connect_ex((adress,port))
		if isConnected == 0:
			print(Fore.WHITE + "-------------------------")
			print(Fore.CYAN + f"Port {port} is open")
			open_port_number += 1
		else:
			pass
		
	print(Fore.WHITE + "-------------------------\n")
	print(Fore.RED + f"{open_port_number} port(s) open at {adress}\n")
	s.close()


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--adress', help='Specify the address', required=True)
parser.add_argument('--end-port',help="The port at which the port scan will end",required=False,default=100)
parser.add_argument('-t','--timeout',help="Timeout count",required=False,default=1)
args = parser.parse_args()


if __name__ == "__main__":
	scan(args.adress,args.end_port,args.timeout)
