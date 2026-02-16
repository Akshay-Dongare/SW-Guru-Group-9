BEGIN { FS = "," }
NR == 1 { expected = NF; next }
NF != expected { n++; print NR }
END { print n + 0 > "/dev/stderr" }