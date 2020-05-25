



class Proxy:
    def __init__(self, ip, port, email, domain):
        self.ip = ip
        self.email = email
        self.port = port
        self.domain = domain

    
# p1 = Proxy("139.59.45.123", None, "admin@verifyleads.io", "api.verifyleads.io")
# p2 = Proxy("167.71.225.82", 4444, "dev@verifyleads.io", "verifyleads.io")
proxies = [Proxy("139.59.45.123", None, "admin@verifyleads.io", "api.verifyleads.io"),
Proxy("167.71.225.82", 4444, "dev@verifyleads.io", "verifyleads.io")
]