# Story v07 music: original, generated with numpy. 124 bpm, B minor / D major, vi-IV-I-V (Bm G D A),
# marimba arps, bouncing octave bass, 16th shaker, four-on-the-floor kick, finger snaps, bell hook.
import numpy as np, wave, sys
sr=44100; bpm=124; beat=60/bpm; dur=15.0; N=int(sr*dur)
out=np.zeros((N,2)); rng=np.random.default_rng(2611)
def add(sig,t,pan=0.0,gain=1.0):
    i=int(t*sr)
    if i>=N: return
    s=sig[:N-i]*gain
    out[i:i+len(s),0]+=s*(1-pan)*0.707; out[i:i+len(s),1]+=s*(1+pan)*0.707
def hz(m): return 440*2**((m-69)/12)
def kick():
    n=int(.3*sr); t=np.arange(n)/sr; f=45+110*np.exp(-t*40)
    return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-t*11)
def snap():
    n=int(.12*sr); t=np.arange(n)/sr; x=rng.standard_normal(n)
    x=x-np.convolve(x,np.ones(12)/12,'same')
    return x*np.exp(-t*45)*0.6
def shaker(acc):
    n=int(.05*sr); t=np.arange(n)/sr; x=rng.standard_normal(n); x=np.diff(np.concatenate([[0],x]))
    a=np.minimum(1,t/0.01)
    return x*a*np.exp(-t*60)*(0.16 if acc else 0.08)
def marimba(f,length=.5):
    n=int(length*sr); t=np.arange(n)/sr
    s=np.sin(2*np.pi*f*t)*np.exp(-t*7)+.35*np.sin(2*np.pi*4*f*t)*np.exp(-t*30)
    return s*np.minimum(1,t/0.002)*0.2
def bass(f,length):
    n=int(length*sr); t=np.arange(n)/sr
    s=np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t)
    return s*np.minimum(1,t/0.005)*np.exp(-t*5)*0.38
def bell(f,length=.6):
    n=int(length*sr); t=np.arange(n)/sr
    s=np.sin(2*np.pi*f*t+1.6*np.sin(2*np.pi*3.5*f*t)*np.exp(-t*6))
    return s*np.minimum(1,t/0.003)*np.exp(-t*4)*0.09
def pad(ch,length):
    n=int(length*sr); t=np.arange(n)/sr
    s=sum(np.sin(2*np.pi*hz(m)*d*t) for m in ch for d in (1,1.003))/ (2*len(ch))
    return s*np.minimum(1,t/0.6)*np.minimum(1,(length-t)/0.3)*0.06
chords=[[59,62,66],[55,59,62],[62,66,69],[57,61,64]]   # Bm G D A
roots=[35,31,38,33]
hook=[(0,74),(0.75,73),(1.5,71),(2.5,69),(3,71)]        # bell motif (beats, midi)
bar=4*beat; bars=int(np.ceil(dur/bar))
for b in range(bars):
    ch=chords[b%4]; r=roots[b%4]; t0=b*bar
    add(pad(ch,bar),t0)
    pat=[ch[0],ch[2],ch[1]+12,ch[2],ch[0]+12,ch[2],ch[1]+12,ch[2]]
    for i,m in enumerate(pat): add(marimba(hz(m+12)),t0+i*beat/2,(.35 if i%2 else -.35))
    for i in range(8):  # octave bounce bass on 8ths
        add(bass(hz(r+(12 if i%2 else 0)),beat/2),t0+i*beat/2)
    if b>=1:
        for k in range(4):
            add(kick(),t0+k*beat,0,0.85)
            if k in (1,3): add(snap(),t0+k*beat,0.1,0.7)
        for s in range(16): add(shaker(s%4==2),t0+s*beat/4,-0.25)
    if b>=2 and b%2==0:
        for (bt,m) in hook: add(bell(hz(m+12)),t0+bt*beat,0.2)
t=np.arange(N)/sr
out*=(np.minimum(1,t/0.6)*np.minimum(1,(dur-t)/1.5))[:,None]
out/=np.max(np.abs(out)); out*=0.63    # peak about -4 dBFS
fn=sys.argv[1] if len(sys.argv)>1 else 'music.wav'
w=wave.open(fn,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close(); print('ok',fn)
