import subprocess
import parser

server_ip = "127.0.0.1"


def client(server_ip):
    process = subprocess.Popen(
        ["iperf3", "-c", server_ip, "-i", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0 and not stderr:
        stderr = f"iperf3 завершився з кодом {process.returncode}"
    return stdout, stderr


result, error = client(server_ip)

if error:
    print(error.strip())
else:
    result_list = parser.parser(result)
    for value in result_list:
        if value["Transfer"] > 2 and value["Bitrate"] > 20:
            print(value)