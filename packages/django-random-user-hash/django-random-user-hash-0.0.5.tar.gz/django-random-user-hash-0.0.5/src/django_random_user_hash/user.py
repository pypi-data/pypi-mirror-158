import hashlib
import random




class User:
    first: str
    last: str
    email: str
    password1: str
    password2: str
    username: str

    def __init__(self,f,l,e,p1,p2,u):
        self.first = f
        self.last = l
        self.email = e
        self.password1 = p1
        self.password2 = p2
        self.username = u

    def gen_seed_value(self,salt:int) -> int:
        x = {
            "1":self.first,
            "2":self.last,
            "3":self.email,
            "4":self.password1,
            "5":self.password2,
            "6":self.username
        }
        seed = 0
        for attr in x:
            seed += self.attr_int_value(x[attr])
        return seed + salt

    def attr_int_value(self, attr) -> list:
        value = 0
        for c in attr:
            value += ord(c)
        return value

    def as_attr_list(self,) -> list:
        attr_list = [
            self.first,
            self.last,
            self.email,
            self.password1,
            self.password2,
            self.username
        ]
        return attr_list

    def test(self,) -> str:
        return "This is a testMessage"

    def gen_sha1(self,level: int,salt: int) -> str:
        seed = self.gen_seed_value(salt=salt)
        random.seed(a=seed,version=level)
        order = [random.randint(0,5) for i in range(0,6)]        
        attrs = self.as_attr_list()
        hash_str = ""
        for o in order:
            hash_str += attrs[o]
        return hashlib.sha1(bytes(hash_str,'utf-8')).hexdigest()