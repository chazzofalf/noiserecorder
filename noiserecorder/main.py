def main():   
    version='0.0'
    product='Noise Recorder'
    author='Charles T. Montgomery'
    email='charles.montgomery@charter.net'
    description='Securely records sound using a microphone and generates noise using the least significant bit of each sample for each channel'
    invocation1='noiserecorder --help'
    invocation1Description='Generates this help message'
    invocation2='noiserecorder'
    invocation2Description='Generates 30 minutes (notice that this will take about 8 hours) of noise written to a dated file.'
    invocation3='noiserecorder pathname/filename.wav'
    invocation3Description='Generates 30 minutes of noise written to a specific path.'
    invocation4='noiserecorder pathname/filename.wav <duration_in_seconds>'
    invocation4Description='Generates specified duration of noise written to a specific path.'
    mesg=[f'{product} v. {version}\n',
          f'{author} ({email})\n',
          f'{description}\n',
          'Invocation:\n',
          f'{invocation1}\n',
          f'\t{invocation1Description}\n',
          f'{invocation2}\n',
          f'\t{invocation2Description}\n',
          f'{invocation3}\n',
          f'\t{invocation3Description}\n',
          f'{invocation4}\n',
          f'\t{invocation4Description}']
    mesg = '\n'.join(mesg)
    mesg = bytes(mesg,encoding='utf8')    
    invalid=False
    from sys import argv 
    from sys import stderr   
    if len(argv) == 2 and argv[1] == '--help':
        stderr.buffer.write(mesg)
        stderr.buffer.flush()
    else:
        from datetime import datetime
        tz=str(datetime.utcnow().astimezone().tzinfo)
        now_=datetime.now(tz=tz) # Use the timezone. We are getting bad errors at 5PM (The interpreter things it is 11PM at 5PM for some reason otherwise)!
        time_default=30*60
        year=now_.year
        month=now_.month
        day=now_.day
        hour=now_.hour
        minute=now_.minute
        second=now_.second
        micros=now_.microsecond
        (year,month,day,hour,minute,second,micros) = tuple((str(f)  for f in (year,month,day,hour,minute,second,micros)))
        (year,month,day,hour,minute,second,micros) = zip((year,month,day,hour,minute,second,micros),(int(4),int(2),int(2),int(2),int(2),int(2),int(6)))
        def pad(strnum,size):
            out = None
            if isinstance(strnum,str) and isinstance(size,int):            
                out=''.join(reversed((''.join(reversed(strnum)) + '0'*size)[:size]))
            return out
                
        (year,month,day,hour,minute,second,micros) = tuple((pad(f[0],f[1]) for f in (year,month,day,hour,minute,second,micros)))
        file_default='noiserecorder_' + ''.join((year,month,day)) + '_' + ''.join((hour,minute,second)) + '_' + micros + '.wav'
        (file,time)=(file_default,time_default)    
        if len(argv) >= 2:        
            file=argv[1]
            
        if len(argv) == 3:        
            time_str=argv[2]
            try:
                time=int(time_str)
            except:
                invalid=True
        elif len(argv) != 1:
            invalid=True
        if invalid:
            tab=' '*4
            msg = 'Invalid Arguments:\n' +\
            tab + 'Invocation:' +\
            tab*2 + 'python -m noiserecorder <filename> [time_in_seconds]' +\
            tab*3 + 'Note: obmission of time_in_seconds means ' + str(30*60) + ' seconds'
            msg = bytes(msg,encoding='utf8')
            from sys import stderr
            stderr.buffer.write(msg)
            stderr.buffer.flush()
        else:        
            from noiserecorder.noiserecorder import savenoisefile as snf
            tab=' '*4
            msg = 'Recording ' + str(time) + ' second long noise the following file: ' + file + '\n' +\
                'This will take ' + str(time*16) + ' seconds.'
            msg = bytes(msg,encoding='utf8')
            from sys import stderr
            stderr.buffer.write(msg)
            stderr.buffer.flush()        
            snf(file,time)


if __name__ == '__main__':
    from noiserecorder.main import main
    main()