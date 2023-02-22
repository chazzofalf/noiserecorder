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
def checkrecoverypassword(name:str,recovery_password:str) -> bool:
    kf = FileIO(file=f'{name}.key',mode='r')
    return checkrecoverypassword_(recovery_password,kf)
def checkrecoverypassword_(recovery_password:str,kf:FileIO) -> bool:
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
    meth_in=cipher.decrypt    
    keydata=meth_in(kf.readall())        
    kf.close()
    valid = True
    for _ in range(0,3):
        hash1,keydata = (bytes(keydata[:32]),bytes(keydata[32:]))
        dehasher=hash()
        dehasher.update(keydata)
        vhash=dehasher.digest()
        def compareblocks(blockA,blockB):            
            if len(blockA) == len(blockB):
                def equal(a,b) -> bool:                     
                    return a == b
                for ff in (f for f in map( equal,blockA,blockB)):
                    if not ff:
                        return ff
                return True
            else:
                return False        
        if not compareblocks(hash1,vhash):
            valid = False
            break     
    return valid
def recovernoise(output:RawIOBase,recovery_password:str,kf:FileIO,tf:FileIO):  
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
    meth_in=cipher.decrypt    
    keydata=meth_in(kf.readall())        
    kf.close()
    valid = True
    for _ in range(0,3):
        hash1,keydata = (bytes(keydata[:32]),bytes(keydata[32:]))
        dehasher=hash()
        dehasher.update(keydata)
        vhash=dehasher.digest()
        def compareblocks(blockA,blockB):
            if len(blockA) == len(blockB):
                def equal(a,b) -> bool:
                    return a == b
                for ff in (f for f in map( equal,blockA,blockB)):
                    if not ff:
                        return ff
                return True
            else:
                return False
        if not compareblocks(hash1,vhash):
            valid = False
            break     
    if valid: 
        keydata = (keydata[4096:])
        key = keydata[:32]
        iv = keydata[32:]
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
            idx=0        
            tf.seek(0)
            cipher = AES.new(key=key,IV=iv,mode=AES.MODE_CBC)        
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
def savenoise(output:RawIOBase,recovery_password:str,kf:FileIO,tf:FileIO,time:int):        
    rp=bytes(recovery_password,encoding='utf8')
    from Crypto.Hash.SHA256 import new as hash
    from Crypto.Random import get_random_bytes as grb
    ho=hash()
    ho.update(rp)
    rp=ho.digest()
    rkk=rp          
    from Crypto.Cipher import AES 
    
    cipher = AES.new(key=rkk,mode=AES.MODE_EAX)    
    meth_out=cipher.encrypt_and_digest   
    from sounddevice import RawInputStream as ris
    from time import sleep as sleepx
    import wave
    with wave.open(output,mode='wb') as wfa:                
        key=grb(32)
        iv=grb(16)
        salt=grb(4096)
        def combo():
            def c1():
                for f in [salt,rkk]:
                    for ff in f:
                        yield ff
            b=bytes([f for f in c1()])
            for _ in range(0,3):
                hclhh=hash()
                hclhh.update(b)
                h=hclhh.digest()
                def c2():
                    for f in [h,b]:
                        for ff in f:
                            yield ff
                b = bytes([f for f in c2()])
            return b
        kfc=bytes([f for f in combo()]) 
        c,m = meth_out(kfc)        
        mlen=len(m)
        clen=len(c)
        mlen=bytes([m/256,m%256])  
        clen=bytes([c/256,c%256])
        def cmblock():
            for f in [mlen,m,clen,c]:
                for ff in f:
                    yield ff   
        cmblock=bytes([f for f in cmblock()])
        cmblocklen=len(cmblock)
        cmblocklen=bytes(cmblocklen/256,cmblocklen%256)
        def cmblock():
            for f in [cmblocklen,cmblock]:
                for ff in f:
                    yield ff
        cmblock=bytes([f for f in cmblock()])
        kf.write(cmblock)                    
        kf.flush()
        kf.close()        
        cipher = AES.new(key=key,mode=AES.MODE_EAX)
        meth_out = cipher.encrypt_and_digest
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
        idx=0
        tf_buf=bytearray()
        def tf_write(ind):
            tf_buf.extend(bytes(ind))
            while len(tf_buf) >= 1 << 15:
                data=bytes(tf_buf[:1<<15])
                remainder=bytes(tf_buf[1<<15:])
                tf_buf.clear()
                tf_buf.extend(remainder)
                c,m = cipher.encrypt_and_digest(data)
                mlen=len(m)
                clen=len(c)
                mlen=bytes([m/256,m%256])  
                clen=bytes([c/256,c%256])
                def cmblock():
                    for f in [mlen,m,clen,c]:
                        for ff in f:
                            yield ff   
                cmblock=bytes([f for f in cmblock()])
                cmblocklen=len(cmblock)
                cmblocklen=bytes(cmblocklen/256,cmblocklen%256)
                def cmblock():
                    for f in [cmblocklen,cmblock]:
                        for ff in f:
                            yield ff
                cmblock=bytes([f for f in cmblock()])
                kf.write(cmblock)                   
                tf_buf.clear()
        def cb(ind,frames,time,status):
            tf_write(ind)            
        with ris(samplerate=44100,dtype='int16',channels=2,callback=cb) as ss:
            sleepx(time*16)
        tf.seek(0)
        cipher = AES.new(key=key,mode=AES.MODE_EAX)
        meth_out = cipher.encrypt        
        meth_in = cipher.decrypt_and_verify
        def get_block():
            size=tf.read(2)
            if len(size) == 2:
                size = size[0]*256+size[1]
            else:
                raise IOError()
            cmblock=tf.read(size)
            if len(cmblock) != size:
                raise IOError()
            from io import BytesIO
            tfi = BytesIO(cmblock)
            size = tfi.read(2)
            if len(size) == 2:
                size=size[0]*256+size[1]
            else:
                raise IOError()
            m = tfi.read(size)
            if len(m) != size:
                raise IOError()
            size=tf.read(2)
            if len(size) == 2:
                size = size[0]*256+size[1]
            else:
                raise IOError()
            c = tfi.read(size)
            if len(c) != size:
                raise IOError()
            return meth_in(c,m)        
        ind =  get_block()
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
            ind = get_block()
        if len(bytesbuff) > 0:
            wf.writeframesraw(bytesbuff)
            wf.close()
    tf.close()    
def savenoisefile(name:str,time:int,recovery_password:str):
    f = FileIO(file=name,mode='w')
    kf = FileIO(file=f'{name}.key',mode='w')    
    tf = FileIO(file=f'{name}.tmp',mode='w+')
    savenoise(f,recovery_password,kf,tf,time)    
    f.close()    
    from os import remove
    _ = [remove(f) for f in [kf.name,tf.name]]
def recovernoisefile(name:str,recovery_password:str):
    f = FileIO(file=name,mode='w')
    kf = FileIO(file=f'{name}.key',mode='r')    
    tf = FileIO(file=f'{name}.tmp',mode='r')
    recovernoise(f,recovery_password,kf,tf)
    f.close()
    