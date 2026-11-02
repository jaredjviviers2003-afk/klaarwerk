import numpy as np, wave
sr=44100; bpm=112; beat=60/bpm; dur=15.0; N=int(sr*dur)
out=np.zeros((N,2))
rng=np.random.default_rng(7)
def add(sig,t,pan=0.0,gain=1.0):
    i=int(t*sr); s=sig[:max(0,min(len(sig),N-i))]*gain
    out[i:i+len(s),0]+=s*(1-pan)*0.5*2**0.5; out[i:i+len(s),1]+=s*(1+pan)*0.5*2**0.5
def env(n,a=0.005,d=0.3):
    t=np.arange(n)/sr; e=np.minimum(1,t/a)*np.exp(-t/d); return e
def kick():
    n=int(.35*sr); t=np.arange(n)/sr; f=50+90*np.exp(-t*30)
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*9)
def clap():
    n=int(.25*sr); t=np.arange(n)/sr; x=rng.standard_normal(n)
    b=np.convolve(x,np.ones(6)/6,'same')-np.convolve(x,np.ones(40)/40,'same')
    return b*np.exp(-t*18)*0.8
def hat():
    n=int(.06*sr); x=rng.standard_normal(n); x=np.diff(np.concatenate([[0],x]))
    return x*np.exp(-np.arange(n)/sr*70)*0.25
def tone(freq,length,kind='pluck'):
    n=int(length*sr); t=np.arange(n)/sr
    if kind=='pluck':
        s=np.sin(2*np.pi*freq*t)+.5*np.sin(2*np.pi*2*freq*t)+.25*np.sin(2*np.pi*3*freq*t)
        return s*env(n,.003,.22)*0.22
    if kind=='bass':
        s=np.tanh(2*np.sin(2*np.pi*freq*t))
        return s*env(n,.004,.35)*0.35
    if kind=='pad':
        s=sum(np.sin(2*np.pi*freq*d*t) for d in (1,1.004,0.996))/3
        a=np.minimum(1,t/0.4)*np.minimum(1,(length-t)/0.4)
        return s*a*0.07
def hz(m): return 440*2**((m-69)/12)
# I-V-vi-IV in C: C G Am F
chords=[[60,64,67],[55,59,62],[57,60,64],[53,57,60]]
roots=[36,43,45,41]
bars=int(np.ceil(dur/(4*beat)))
for b in range(bars):
    ch=chords[b%4]; r=roots[b%4]; t0=b*4*beat
    for nte in ch: add(tone(hz(nte),4*beat,'pad'),t0,0)
    for i,s in enumerate([0,1.5,2,3.5]): add(tone(hz(r),.4,'bass'),t0+s*beat)
    arp=[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+12]*2
    for i,nte in enumerate(arp):
        if t0+i*beat/2>=0.0: add(tone(hz(nte),.35,'pluck'),t0+i*beat/2,(-.4 if i%2 else .4))
    for k in range(4):
        tb=t0+k*beat
        if b>0 or k>=2: add(kick(),tb,0,0.9)
        if k in (1,3) and b>0: add(clap(),tb,0,0.5)
        for h in (0.5,):
            if b>0: add(hat(),tb+h*beat,0.3)
# fades
t=np.arange(N)/sr
out*= (np.minimum(1,t/0.3)*np.minimum(1,(dur-t)/1.5))[:,None]
out/=np.max(np.abs(out))*1.12
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close(); print('ok')
