import csv_writer
import pyad.adquery

q = pyad.adquery.ADQuery()
q.execute_query(attributes=["distinguishedName", "description"], where_clause="objectClass = 'computer'")
headers = ["host_found"]
pattern_hostname = "el"
hosts_found = []

for row in q.get_results():
    str_split = row["distinguishedName"].split(",")
    str_split = str_split[0].split("=")
    hostname = str_split[1].lower()

    if hostname.find(pattern_hostname) is not -1:
        print("Found " + hostname)
        hosts_found.append([hostname])

csv = csv_writer.CsvWriter("output.csv", headers, hosts_found)
csv.create_csv()