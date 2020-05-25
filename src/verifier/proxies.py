



class Proxy:
    def __init__(self, ip, port, email, domain):
        self.ip = ip
        self.email = email
        self.port = port
        self.domain = domain

    
# p1 = Proxy("139.59.45.123", None, "admin@verifyleads.io", "api.verifyleads.io")
# p2 = Proxy("167.71.225.82", 4444, "dev@verifyleads.io", "verifyleads.io")
proxies = [Proxy("139.59.45.123", None, "admin@verifyleads.io", "api.verifyleads.io"),
Proxy("167.71.225.82", 4444, "dev@verifyleads.io", "verifyleads.io"),
Proxy("167.99.230.178", 4445, "p1@verifyleads.io", "p1.verifyleads.io"),
Proxy("138.197.144.42", 4446, "p2@verifyleads.io", "p2.verifyleads.io"),
Proxy("167.99.71.148", 4447, "p3@verifyleads.io", "p3.verifyleads.io"),
Proxy("167.99.179.58", 4448, "p4@verifyleads.io", "p4.verifyleads.io")
]