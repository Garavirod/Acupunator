import hashlib 


class PasswordEncrypt():
    def __init__(self):
        pass

    def encrypt(self,psd):
        encrypted = hashlib.md5(psd.encode()).hexdigest()        
        return encrypted

    def validatepassword(self,pass2,pass1):
        p2  = self.encrypt(pass2)
        if p2 == pass1:
            return True
        else:
            return False

if __name__ == "__main__":
    obj = PasswordEncrypt()
    pass1 = "MD5Online"
    db_pass = "d49019c7a78cdaac54250ac56d0eda8a"

    print(obj.validatepassword(pass1,db_pass))