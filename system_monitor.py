import subprocess
import sys

def uso_cpu():

	top_output=subprocess.getoutput("top -d 1 -b -n2 | grep 'Cpu(s)' | tail -n 1")
	if top_output.find(" id,")>=0:
		top_output=top_output[top_output.find(" id,")-5:top_output.find(" id,")]
	return 100-float(top_output.strip())

def uso_memoria():
	mem_total=subprocess.getoutput("cat /proc/meminfo | grep MemTotal:") 
	mem_available=subprocess.getoutput("cat /proc/meminfo | grep MemAvailable:") 
	mem_total=mem_total.split()[1]
	mem_available=mem_available.split()[1]
	return 100-(100 * float(mem_available)/float(mem_total))

def uso_disco():
	df_output=subprocess.getoutput("df  | awk '{print $2,$3}'")
	max_longitud=(len(df_output.split()))
	contador=2
	cantidades_disponibles=[]
	cantidades_usadas=[]
	while contador < max_longitud:
		cantidades_disponibles.append(int(df_output.split()[contador]))
		cantidades_usadas.append(int(df_output.split()[contador+1]))
		contador=contador+2

	return (100 * sum(cantidades_usadas)/sum(cantidades_disponibles))

def use_mode():
	print("python3 system_monitor.py operación")
	print("Operaciones validas cpu - memoria - disco")

if __name__ == '__main__':
	if len(sys.argv) !=2:
		use_mode()
		exit(1)
	
	operacion = sys.argv[1]

	if operacion=="cpu":
		print("El uso de procesador es del: %.2f%%" % uso_cpu())
	elif operacion=="memoria":
		print("El uso de memoria es del: %.2f%%" % uso_memoria())
	elif operacion=="disco":
		#print(uso_disco())
		print("El uso del disco es del: %.2f%%"% uso_disco())
	else:
		print("Operacion no valida!")
		use_mode()