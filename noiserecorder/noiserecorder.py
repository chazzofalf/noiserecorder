from io import RawIOBase
from io import FileIO
from typing import TypeVar
from typing import Generic
from tempfile import TemporaryFile
C = TypeVar('C')
class Ref(Generic[C]):
    def __init__(self,initial_value=None):
        self.__value:C=initial_value
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self,value):
        self.__value = value


def recovernoise(output:RawIOBase,recovery_password:str,kf:FileIO,ivf:FileIO,tf:FileIO):  
    rp=recovery_password
    rp=bytes(rp,encoding='utf8')
    from time import sleep as sleepx  
    from sounddevice import RawInputStream as ris
    from Crypto.Hash.SHA256 import new as hash
    ho=hash()
    ho.update(rp)
    rp=ho.digest()
    rkk=rp
    ho=hash()
    ho.update(rp)
    rp=ho.digest()
    rp=rp[:16]
    rkiv=rp
    from Crypto.Cipher import AES 
    cipher= AES.new(key=rkk,iv=rkiv,mode=AES.MODE_CBC)
    cipher2= AES.new(key=rkk,iv=rkiv,mode=AES.MODE_CBC)
    meth_in=cipher.decrypt
    meth_in_2=cipher2.decrypt
    key=meth_in(kf.readall())
    iv=meth_in_2(ivf.readall())
    kf.close()
    ivf.close()
    cipher = AES.new(key=key,IV=iv,mode=AES.MODE_CBC)
    meth_in=cipher.decrypt
    import wave
    with wave.open(output,mode='wb') as wfa: 
        wf:wave.Wave_write=wfa
        wf.setframerate(44100)
        wf.setnchannels(2)
        wf.setsampwidth(2)
        bytesbuff=bytearray()
        shortBuffA=bytearray()
        shortBuffB=bytearray()
        shortBuffAO=bytearray()
        shortBuffBO=bytearray()
        byteA=0
        byteB=0
        idxA=0
        idxB=0
        idx=0        
        tf.seek(0)
        cipher = AES.new(key=key,IV=iv,mode=AES.MODE_CBC)
        meth_out = cipher.encrypt
        meth_in = cipher.decrypt
        ind =  meth_in(tf.read(4*44100))
        while ind is not None and len(ind) > 0:
            for f in bytes(ind):                
                if len(shortBuffA) < 2:
                    shortBuffA.append(f)
                else:
                    shortBuffB.append(f)
                if len(shortBuffB) == 2:
                    byteA <<= 1
                    byteB <<= 1
                    byteA |= (shortBuffA[0] & 1)
                    byteB |= (shortBuffB[0] & 1)                
                    shortBuffA.clear()
                    shortBuffB.clear()
                    idx += 1
                if idx == 8:
                    shortBuffAO.append(byteA)
                    shortBuffBO.append(byteB)
                    byteA = 0
                    byteB = 0
                    idx = 0
                if len(shortBuffAO) == 2:
                    bytesbuff.extend(shortBuffAO)
                    bytesbuff.extend(shortBuffBO)    
                    shortBuffAO.clear()
                    shortBuffBO.clear()
                if len(bytesbuff) == 4*44100:
                    wf.writeframesraw(bytesbuff)                
                    bytesbuff.clear()
            ind = tf.read(4*44100)
        if len(bytesbuff) > 0:
            wf.writeframesraw(bytesbuff)
            wf.close()
    tf.close()  
def savenoise(output:RawIOBase,recovery_password:str,kf:FileIO,ivf:FileIO,tf:FileIO,time:int):    
    
    rp=bytes(recovery_password,encoding='utf8')
    from Crypto.Hash.SHA256 import new as hash
    ho=hash()
    ho.update(rp)
    rp=ho.digest()
    rkk=rp
    ho=hash()
    ho.update(rp)
    rp=ho.digest()
    rp=rp[:16]
    rkiv=rp
    from Crypto.Cipher import AES 
    cipher= AES.new(key=rkk,iv=rkiv,mode=AES.MODE_CBC)
    cipher2= AES.new(key=rkk,iv=rkiv,mode=AES.MODE_CBC)
    meth_out=cipher.encrypt
    meth_out_2=cipher2.encrypt
    from sounddevice import RawInputStream as ris
    from time import sleep as sleepx
    import wave
    with wave.open(output,mode='wb') as wfa:        
        from Crypto.Random import get_random_bytes
        key=get_random_bytes(32)
        iv=get_random_bytes(16)
        kf.write(meth_out(key))
        kf.flush()
        kf.close()
        ivf.write(meth_out_2(iv))
        ivf.flush()
        ivf.close()
        cipher = AES.new(key=key,IV=iv,mode=AES.MODE_CBC)
        meth_out = cipher.encrypt
        meth_in = cipher.decrypt
        wf:wave.Wave_write=wfa
        wf.setframerate(44100)
        wf.setnchannels(2)
        wf.setsampwidth(2)
        bytesbuff=bytearray()
        shortBuffA=bytearray()
        shortBuffB=bytearray()
        shortBuffAO=bytearray()
        shortBuffBO=bytearray()
        byteA=0
        byteB=0
        idxA=0
        idxB=0
        idx=0
        def cb(ind,frames,time,status):
            tf.write(meth_out(bytes(ind)))                            
        with ris(samplerate=44100,dtype='int16',channels=2,callback=cb) as ss:
            sleepx(time*16)
        tf.seek(0)
        cipher = AES.new(key=key,IV=iv,mode=AES.MODE_CBC)
        meth_out = cipher.encrypt
        meth_in = cipher.decrypt
        ind =  meth_in(tf.read(4*44100))
        while ind is not None and len(ind) > 0:
            for f in bytes(ind):                
                if len(shortBuffA) < 2:
                    shortBuffA.append(f)
                else:
                    shortBuffB.append(f)
                if len(shortBuffB) == 2:
                    byteA <<= 1
                    byteB <<= 1
                    byteA |= (shortBuffA[0] & 1)
                    byteB |= (shortBuffB[0] & 1)                
                    shortBuffA.clear()
                    shortBuffB.clear()
                    idx += 1
                if idx == 8:
                    shortBuffAO.append(byteA)
                    shortBuffBO.append(byteB)
                    byteA = 0
                    byteB = 0
                    idx = 0
                if len(shortBuffAO) == 2:
                    bytesbuff.extend(shortBuffAO)
                    bytesbuff.extend(shortBuffBO)    
                    shortBuffAO.clear()
                    shortBuffBO.clear()
                if len(bytesbuff) == 4*44100:
                    wf.writeframesraw(bytesbuff)                
                    bytesbuff.clear()
            ind = tf.read(4*44100)
        if len(bytesbuff) > 0:
            wf.writeframesraw(bytesbuff)
            wf.close()
    tf.close()    
def savenoisefile(name:str,time:int,recovery_password:str):
    f = FileIO(file=name,mode='w')
    kf = FileIO(file=f'{name}.key',mode='w')
    ivf = FileIO(file=f'{name}.iv',mode='w')
    tf = FileIO(file=f'{name}.tmp',mode='w+')
    savenoise(f,recovery_password,kf,ivf,tf,time)    
    f.close()    
    from os import remove
    _ = [remove(f) for f in [kf.name,ivf.name,tf.name]]
def recovernoisefile(name:str,recovery_password:str):
    f = FileIO(file=name,mode='w')
    kf = FileIO(file=f'{name}.key',mode='r')
    ivf = FileIO(file=f'{name}.iv',mode='r')
    tf = FileIO(file=f'{name}.tmp',mode='r')
    recovernoise(f,recovery_password,kf,ivf,tf)
    f.close()
    
    
    