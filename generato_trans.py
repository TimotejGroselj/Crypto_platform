import sqlite3 as sql
import random as r
from funkcije_encription import *
conn = sql.connect('cryptodata.sqlite')

with conn:
    cur = conn.cursor()
    querry = """
    DROP TABLE IF EXISTS transactions;
    CREATE TABLE transactions (
    trans_id integer PRIMARY KEY,
	wallet_id VARCHAR(50),
    coin_id VARCHAR(15),
    quantity numeric(15,6) CHECK (quantity > 0),
    date date NOT NULL,
    valid integer CHECK (valid in (0,1)),
    type VARCHAR(4) CHECK (type in ('buy','sell'))
    );
    """
    cur.executescript(querry)
    querry = """
    SELECT wallet_id FROM assets
    GROUP BY wallet_id
    """
    wallets = cur.execute(querry).fetchall()
    querry = """
        SELECT date FROM coins_prices
        GROUP BY date
        """
    dates = cur.execute(querry).fetchall()
    dates.sort()
    m = len(dates)
    for wallet_id in wallets:
        querry = """
        SELECT coin_id, money FROM assets
        WHERE wallet_id = ? AND coin_id != 'EUR'
        """
        data = cur.execute(querry,wallet_id).fetchall()
        for coin_id, quantity in data:
            
            n = r.randint(1,30)
            #kolk transakciji je za ta coin naredu en wallet
            how_many = r.uniform(1,1000)
            summ =  how_many
            investments = [how_many]
            for _ in range(n):
                how_many = r.uniform(-summ,1000)
                summ += how_many
                investments.append(how_many)
            #generiras random investicije kolk je investiru. investicije se bodo v trans dodajale zaporedoma glede na datume zato lahko naslednji element proda največ 
            # -sum vseh trans do zdaj. 
            # zdaj imamo vektor in ga "normiramo" tako da je seštevek elementov enak quantity
            summ = sum(investments)
            investments = [el/(summ/(quantity+0.1)) for el in investments]
            #zdaj se nam vse investicije v coin seštejejo v količino coina ki jo uporabnik ima in so veljavne dokler bojo podatki dodani v pravilnem vrstnem redu, 
            # +0.1 je zato da se pri coinih, katerih končno stanje je 0 izognemo deljenju z 0 in še vseeno dobimo transakcije ki se seštejejo v skoraj 0.
            maxx = -1
            for i in range(n):
                querry = """
                INSERT INTO transactions
                (wallet_id,coin_id,quantity,date,valid,type)
                VALUES (?,?,?,?,?,?)
                """
                ind = r.randint(maxx,m-n+i)
                maxx = ind
                #ustvarimo indeks ki bo uporabljen za določanje datuma. je lahko najmanj isto kot prejšnji določen inddeks, indeks je zgoraj omejen tako da lahko vse transakcije spravimo (sam da bad luck ne cock blocka)
                kok = investments[i]
                cur.execute(querry,(wallet_id[0],coin_id,abs(kok),dates[ind][0],1,'sell' if kok < 0 else 'buy'))
                #še par failanih transakcij
                if i % 4 ==0:
                    if kok<0:
                        cur.execute(querry,(wallet_id[0],coin_id,abs(kok)+r.uniform(0,100),dates[ind][0],0,'sell'))
                    else:
                        cur.execute(querry,(wallet_id[0],coin_id,abs(abs(kok)+r.uniform(-100,100)),dates[ind][0],0,'buy'))
    