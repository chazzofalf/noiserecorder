from io import RawIOBase
from io import FileIO
from typing import TypeVar
from typing import Generic
from tempfile import TemporaryFile
from threading import Thread
from threading import RLock
from time import thread_time
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
class SaveNoise(object):
    def __init__(self) -> None:
        self.__wp=0
        self.__rp=0
        self.__tl=RLock()
        
    def savenoise(self,output:RawIOBase,time:int):  
        
        with TemporaryFile(mode='w+b') as tf:
            
            from sounddevice import RawInputStream as ris
            from time import sleep as sleepx
            import wave
            with wave.open(output,mode='wb') as wfa:
                
                from Crypto.Cipher import AES    
                from Crypto.Random import get_random_bytes
                key=get_random_bytes(32)
                iv=get_random_bytes(16)
                cipher = AES.new(key=key,IV=iv,mode=AES.MODE_CBC)
                meth_out = cipher.encrypt
                meth_in = cipher.decrypt
                wf:wave.Wave_write=wfa
                wf.setframerate(44100)
                wf.setnchannels(2)
                wf.setsampwidth(2)
                
                
                
                def write_it(b:bytes):
                    self.__tl.acquire()            
                    tf.seek(self.__wp)
                    out = tf.write(b) 
                    self.__wp += len(b)
                    #print(f'wp={self.__wp}')
                    self.__tl.release()
                    return out
                def read_it(size:int):
                    self.__tl.acquire()
                    tf.seek(self.__rp)
                    out = tf.read(size)
                    self.__rp += len(out)
                    #print(f'rp={self.__rp}')
                    self.__tl.release()
                    return out
                def cb(ind,frames,time,status):   
                    write_it(meth_out(bytes(ind))) 
                    
                    
                def cat(a,b):
                    yield from a
                    yield from b
                def read_task():
                    idx=0
                    byteA=0
                    byteB=0
                    shortBuffA=bytearray()
                    shortBuffB=bytearray()
                    shortBuffAO=bytearray()
                    shortBuffBO=bytearray()
                    bytesbuff=bytearray()
                    buf=bytearray()
                    size_max=44112*4
                    ts=0.0
                    cipher=AES.new(key=key,IV=iv,mode=AES.MODE_CBC)
                    meth_in = cipher.decrypt              
                    r_data = read_it(size_max)
                    while len(r_data) > 0 or not write_finished:
                        if not write_finished:
                            ts=thread_time()
                        if len(r_data) > 0 and len(r_data) % cipher.block_size != 0:
                            r_data=bytearray(r_data)
                            while len(r_data) % cipher.block_size != 0:
                                rr_data = read_it(1)
                                if len(rr_data) == 1:
                                    r_data.extend(rr_data)
                                elif write_finished:
                                    raise 'Incomplete Block!'
                            r_data=bytes(r_data)
                        r_data=meth_in(r_data) if len(r_data) > 0 else r_data
                        if len(r_data) > 0:
                            r_data = meth_in(r_data)
                            buf.extend(r_data)                                                        
                            for f in r_data:                                
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
                                if len(bytesbuff) == size_max/4:
                                    wf.writeframesraw(bytesbuff)                
                                    bytesbuff.clear()
                                
                        r_data = read_it(size_max)                        
                        if not write_finished:
                            te=thread_time()
                            td=te-ts
                            st=td*100
                            sleepx(st)
                    if len(bytesbuff) > 0:
                        wf.writeframesraw(bytesbuff)
                    wf.close()                    
                write_finished=False       
                t:Thread=None                
                with ris(samplerate=44100,dtype='int16',channels=2,callback=cb) as ss:    
                    t=Thread(group=None,target=read_task)               
                    t.start()                 
                    sleepx(time*16)
                write_finished=True
                t.join()
                
    def savenoisefile(self,name:str,time:int):
        f = FileIO(file=name,mode='w')
        self.savenoise(f,time)
        f.close()
    
    