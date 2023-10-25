# Port Scanner
Simple port scanner script written in python.
It is not pratical to use this I just created it for fun.
Script just checks if port is listening or not.

## Args
* Takes first argument as target host.
* `-p`, defines port range to scan. (ex: -p 500-1000, -p 600 -, -p - 500, -p - -)
* `-t`, defines timeout for each port scan (default: 0.5)
* `-w`, defines maximum worker thread count that runs simultaneously. (default: 200)