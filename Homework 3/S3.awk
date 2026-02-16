BEGIN { FS="," }
NR==1 { split($0,H,","); next } NR==2 { split($0,v,","); for(i in v) k[i]=1; next }
{ for(i in k) if($i!=v[i]) delete k[i] }
END { for(i=1;i<=length(H);i++) if(i in k) { print H[i]; c++ } print c+0 > "/dev/stderr" }