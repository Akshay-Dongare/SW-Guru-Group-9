BEGIN { FS = "," }
NR==1 { split($0, H, ","); next }
{ for(i=1;i<=NF;i++) if($i=="?") { C[H[i]]; if(!seen[NR]++) { buf = buf "row: " NR "\n"; n++ } } }
END { for(c in C) print "col: " c; printf "%s", buf; print n+0 > "/dev/stderr" }