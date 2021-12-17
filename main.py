import csv_writer
import pyad.adquery
import socket


def check_port(hst, prt):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        host_ip = socket.gethostbyname(hst)

    except socket.gaierror:
        return False

    try:
        host_ip = socket.gethostbyname(hst)

    except socket.gaierror:
        return False

    try:
        s.connect((hst, prt))

    except TimeoutError:
        return False

    except socket.gaierror:
        return False

    except ConnectionRefusedError:
        return False

    return True

q = pyad.adquery.ADQuery()
q.execute_query(attributes=["distinguishedName", "description"], where_clause="objectClass = 'computer'")
headers = ["hostname", "ip_address", "os"]
pattern_hostname = ["el", "los", "audi"]
hosts_found = []

for row in q.get_results():
    str_split = row["distinguishedName"].split(",")
    str_split = str_split[0].split("=")
    hostname = str_split[1].lower()

    for c_patt in pattern_hostname:
    	host_invalid = False
    	if hostname.find(c_patt) is not -1:
        	print("Found " + hostname)

        	try:
        		ip_address = socket.gethostbyname(hostname)

        	except socket.gaierror:
        		ip_address = "host_invalid"
        		host_invalid = True

        	is_windows = check_port(hostname, 3389)

        	if is_windows is True:
        		os = "Windows"

        	else:
        		if host_invalid is False:
        			os = "Linux"

        		else:
        			os = "N/A"


        	hosts_found.append([hostname, ip_address, os])

csv = csv_writer.CsvWriter("output.csv", headers, hosts_found)
csv.create_csv()