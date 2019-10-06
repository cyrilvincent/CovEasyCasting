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
    #res = "Nom" in s
    p.close()
    return res


print("TestPing")
print("========")
prefix = "192.168.1."
r = list(range(2,254))
print(f"Nslookup {prefix}{r}")
res = []
for i in r:
    host = prefix+str(i)
    if nslookup(host):
        print(f"Found {i}")
        res.append(host)
print(res)










