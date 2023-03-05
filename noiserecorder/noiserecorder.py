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
    tf = FileIO(file=f'{name}.tmp',mode='r')
    valid = checkrecoverypassword_(recovery_password,tf)
    tf.close()
    return valid
def checkrecoverypassword_(recovery_password:str,tf:FileIO) -> bool:
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
    rnonce=rp[:16]
    from Crypto.Cipher import AES 
    cipher= AES.new(key=rkk,nonce=rnonce,mode=AES.MODE_EAX)
    def read_block_univ(file:FileIO,meth_in):
        size=file.read(2)
        if len(size) == 0:
            return size
        if len(size) == 2:
            size = size[0]*256+size[1]
        else:
            raise IOError()
        cmblock=file.read(size)
        if len(cmblock) != size:
            raise IOError()
        from io import BytesIO
        tfi = BytesIO(cmblock)
        size = tfi.read(2)
        if len(size) == 2:
            size = size[0]*256 + size[1]
        else:
            raise IOError()
        n = tfi.read(size)
        if len(n) != size:
            raise IOError()
        size = tfi.read(2)
        if len(size) == 2:
            size=size[0]*256+size[1]
        else:
            raise IOError()
        m = tfi.read(size)
        if len(m) != size:
            raise IOError()
        size=tfi.read(2)
        if len(size) == 2:
            size = size[0]*256+size[1]
        else:
            raise IOError()
        c = tfi.read(size)
        if len(c) != size:
            raise IOError()
        return meth_in(c,m)    
    meth_in=cipher.decrypt_and_verify    
    try:
        _=read_block_univ(tf,meth_in) 
        return True        
    except:
       return False    
def recovernoise(output:RawIOBase,recovery_password:str,tf:FileIO):  
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
    rnonce=rp[:16]
    from Crypto.Cipher import AES 
    cipher= AES.new(key=rkk,nonce=rnonce,mode=AES.MODE_EAX)
    def read_next_valid_block(file:FileIO,key):
        # For recovery. 
        # There is chance the program was forcibly closed and there may be a
        # bad/partial block at the end of the file as of result. 
        # This helps ensure they are ignored and do not break the recovery process.
        valid=False
        valid_block=None
        block=None
        while not valid:
            try:
                block=read_block_univ(file,key)
                valid=True
                valid_block=block
            except:
                print('Partial Block Found. This was ignored.')
        return valid_block
            
    def read_block_univ(file:FileIO,key):
        size=file.read(2)
        if len(size) == 0:
            return size
        if len(size) == 2:
            size = size[0]*256+size[1]
        else:
            raise IOError()
        cmblock=file.read(size)
        if len(cmblock) != size:
            raise IOError()
        from io import BytesIO
        tfi = BytesIO(cmblock)
        size = tfi.read(2)
        if len(size) == 2:
            size = size[0]*256 + size[1]
        else:
            raise IOError()
        n = tfi.read(size)
        if len(n) != size:
            raise IOError()
        size = tfi.read(2)
        if len(size) == 2:
            size=size[0]*256+size[1]
        else:
            raise IOError()
        m = tfi.read(size)
        if len(m) != size:
            raise IOError()
        size=tfi.read(2)
        if len(size) == 2:
            size = size[0]*256+size[1]
        else:
            raise IOError()
        c = tfi.read(size)
        if len(c) != size:
            raise IOError()
        cipher= AES.new(key=key,nonce=n,mode=AES.MODE_EAX)
        return cipher.decrypt_and_verify(c,m)          
    keydata=read_block_univ(tf,rkk)           
    valid = True    
    if valid:         
        key = keydata               
        
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
            ind =  read_next_valid_block(tf,key)
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
                ind = read_next_valid_block(tf,key)
            if len(bytesbuff) > 0:
                wf.writeframesraw(bytesbuff)
                wf.close()
        tf.close()                     
def savenoise(output:RawIOBase,recovery_password:str,tf:FileIO,time:int,progress_report:list=None):        
    rp=bytes(recovery_password,encoding='utf8')
    from Crypto.Hash.SHA256 import new as hash
    from Crypto.Random import get_random_bytes as grb
    ho=hash()
    ho.update(rp)
    rp=ho.digest()
    rkk=rp   
    ho=hash()
    ho.update(rp)
    rp=ho.digest()
    rnonce=rp[:16]       
    from Crypto.Cipher import AES 
    
    cipher = AES.new(key=rkk,nonce=rnonce,mode=AES.MODE_EAX)    
    
    meth_out=cipher.encrypt_and_digest   
    from sounddevice import RawInputStream as ris
    from time import sleep as sleepx
    import wave
    with wave.open(output,mode='wb') as wfa:                
        key=grb(32)        
        def keynonce():
            for f in  [key,]:
                for ff in f:
                    yield ff
                         
        c,m = meth_out(bytes([f for f in keynonce()]))    
        n = cipher.nonce    
        mlen=len(m)
        clen=len(c)
        nlen=len(n)
        mlen=bytes([mlen//256,mlen%256])  
        clen=bytes([clen//256,clen%256])
        nlen=bytes([nlen//256,nlen%256])
        def cmblock():
            for f in [nlen,n,mlen,m,clen,c]:
                for ff in f:
                    yield ff   
        cmblock_=bytes([f for f in cmblock()])
        cmblocklen=len(cmblock_)
        cmblocklen=bytes([cmblocklen//256,cmblocklen%256])
        def cmblock():
            for f in [cmblocklen,cmblock_]:
                for ff in f:
                    yield ff
        cmblock_=bytes([f for f in cmblock()])
        tf.write(cmblock_)                                    
        cipher = AES.new(key=key,mode=AES.MODE_EAX)
        meth_out = cipher.encrypt_and_digest
        meth_in = cipher.decrypt
        cipher.update(bytes([]))
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
        read_bytes=[0]
        def tf_write(ind):
            ind_bytes=bytes(ind)
            read_bytes[0] += len(ind_bytes)
            tf_buf.extend(ind_bytes)
            while len(tf_buf) >= 1 << 15:
                data=bytes(tf_buf[:1<<15])
                remainder=bytes(tf_buf[1<<15:])
                tf_buf.clear()
                tf_buf.extend(remainder)
                cipher = AES.new(key=key,mode=AES.MODE_EAX)
                c,m = cipher.encrypt_and_digest(data)
                n = cipher.nonce
                mlen=len(m)
                clen=len(c)
                nlen=len(n)
                mlen=bytes([mlen//256,mlen%256])  
                clen=bytes([clen//256,clen%256])
                nlen=bytes([nlen//256,nlen%256])
                def cmblock():
                    for f in [nlen,n,mlen,m,clen,c]:
                        for ff in f:
                            yield ff   
                cmblock_=bytes([f for f in cmblock()])
                cmblocklen=len(cmblock_)
                cmblocklen=bytes([cmblocklen//256,cmblocklen%256])
                def cmblock():
                    for f in [cmblocklen,cmblock_]:
                        for ff in f:
                            yield ff
                cmblock_=bytes([f for f in cmblock()])
                tf.write(cmblock_)                                   
                tf_buf.clear()
        
        def cb(ind,frames,time,status):            
            tf_write(ind)  
        total_bytes=time*16*44100*2*2       
        with ris(samplerate=44100,dtype='int16',channels=2,callback=cb) as ss:
            while read_bytes[0] < total_bytes:   
                sleepx(0.01)
                if progress_report is not None and len(progress_report) == 1:
                    progress_report[0]=int(read_bytes[0]/total_bytes*10000)/100                             
                
        def tf_flush():
            while len(tf_buf) > 0:
                data=bytes(tf_buf[:1<<15])
                remainder=bytes(tf_buf[1<<15:])
                tf_buf.clear()
                tf_buf.extend(remainder)
                cipher = AES.new(key=key,mode=AES.MODE_EAX)
                
                c,m = cipher.encrypt_and_digest(data)
                n = cipher.nonce
                mlen=len(m)
                clen=len(c)
                nlen=len(n)
                mlen=bytes([mlen//256,mlen%256])  
                clen=bytes([clen//256,clen%256])
                nlen=bytes([nlen//256,nlen%256])
                def cmblock():
                    for f in [nlen,n,mlen,m,clen,c]:
                        for ff in f:
                            yield ff   
                cmblock_=bytes([f for f in cmblock()])
                cmblocklen=len(cmblock_)
                cmblocklen=bytes([cmblocklen//256,cmblocklen%256])
                def cmblock():
                    for f in [cmblocklen,cmblock_]:
                        for ff in f:
                            yield ff
                cmblock_=bytes([f for f in cmblock()])
                tf.write(cmblock_)    
                tf.flush()               
                tf_buf.clear()
        tf_flush()
        tf.seek(0)
        def skip_block():
            size=tf.read(2)
            if len(size) == 0:
                return size
            if len(size) == 2:
                size = size[0]*256+size[1]
            else:
                raise IOError()
            _ = tf.read(size)
        skip_block()
        cipher = AES.new(key=key,mode=AES.MODE_EAX)
        meth_out = cipher.encrypt        
        meth_in = cipher.decrypt_and_verify
        def get_block():
            size=tf.read(2)
            if len(size) == 0:
                return size
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
            n = tfi.read(size)
            if len(n) != size:
                raise IOError()
            size = tfi.read(2)
            if len(size) == 2:
                size=size[0]*256+size[1]
            else:
                raise IOError()
            m = tfi.read(size)
            if len(m) != size:
                raise IOError()
            size=tfi.read(2)
            if len(size) == 2:
                size = size[0]*256+size[1]
            else:
                raise IOError()
            c = tfi.read(size)
            if len(c) != size:
                raise IOError()
            cipher = AES.new(key=key,nonce=n,mode=AES.MODE_EAX)
            return cipher.decrypt_and_verify(c,m)       
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
def savenoisefile(name:str,time:int,recovery_password:str,progress_report:list=None):
    f = FileIO(file=name,mode='w')    
    tf = FileIO(file=f'{name}.tmp',mode='w+')
    savenoise(f,recovery_password,tf,time,progress_report=progress_report)    
    f.close()    
    from os import remove
    _ = [remove(f) for f in [tf.name]]
def recovernoisefile(name:str,recovery_password:str):
    f = FileIO(file=name,mode='w')
    tf = FileIO(file=f'{name}.tmp',mode='r')
    recovernoise(f,recovery_password,tf)
    f.close()
    