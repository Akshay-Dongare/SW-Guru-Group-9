BEGIN { FS = "," }
NR == 1 { next }
seen[$0]++ { n++; print NR }
END { print n + 0 > "/dev/stderr" }