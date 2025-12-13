import sqlite3 as sql
import re
import random
import string


class Login:
    def __init__(self):
        self.conn = sql.connect('cryptodata.sqlite')
        self.cur = self.conn.cursor()

    def valid_login(self,email,password):
        """Preveri, če je uporabnik vnesel pravilno geslo oz email za vstop v platformo"""
        q1 = "SELECT password FROM users WHERE email = ?"
        checker = self.cur.execute(q1,[email]).fetchone()[0]
        if password == checker:
            return True
        return False

    def is_user(self,email):
        """Preveri, če uporabnik že obstaja v bazi"""
        return self.cur.execute('SELECT username FROM users WHERE email = ?',[email]).fetchone() != None
    def valid_email(self,email):
        match = re.findall(r".+@.+\..+", email)
        if not match:
            return False
        return True
    
    def valid_password(self,password):
        strong_password = {'lowercase':0,'uppercase':0,'digit':0,'special':0}
        for i in password:
            if 'a' <= i <= 'z':
                strong_password['lowercase'] += 1
            if 'A' <= i <= 'Z':
                strong_password['uppercase'] += 1
            if '0' <= i <= '9':
                strong_password['digit'] += 1
            else:
                strong_password['special'] += 1
        for key,item in strong_password.items():
            if item < 2:
                return key
        return None
            
            
    def create_user(self,username,email,password=""): #tuki mors se generatat assets zanga
        """Ustvari uporabniški profil"""
        if password == "":
            for i in range(10):
                letter = random.choice(string.printable)
                password += letter
        with self.conn:
            q1 = "INSERT INTO users (username, email, password) VALUES (?,?,?)"
            self.cur.execute(q1,[username,email,password])

    def close(self):
        """Zapremo sejo v temu classu"""
        self.cur.close()
        self.conn.close()










