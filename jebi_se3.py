import pickle
import bcrypt as by
with open(f"data.bin","wb") as data:
    pickle.dump(by.gensalt(5),data)