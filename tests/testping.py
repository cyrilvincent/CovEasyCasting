import os

def ping(host):
    p = os.popen("ping -n 1 " + host)
    s = p.read()
    res = not("perdus = 1" in s)
    p.close()
    return res

def nslookup(ip):
    p = os.popen("nslookup " + ip)
    s = p.read()
    res = "raspberry" in s
    p.close()
    return res


print("TestPing")
print("========")
#r = list(range(0,255))
prefix = "192.168.1."
r = list(range(80,86))
print(f"Ping {prefix}{r}")
res = []
for i in r:
    host = prefix+str(i)
    print(f"Ping {host}")
    if ping(host):
        print("Pinged")
        res.append(host)
print(f"Nslookup {res}")
for i in res:
    if nslookup(i):
        print(f"Found {i}")










