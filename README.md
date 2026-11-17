# File Transfer over TCP and UDP

A programming test assignment implemented by [ST3PAN0V](https://github.com/ST3PAN0V): separate Python clients and servers for transferring a file over TCP and UDP, with Bash scripts for checking the received contents.

## Choose an implementation

| Branch | Contents |
| --- | --- |
| [main](https://github.com/ST3PAN0V/file-transfer-udp-tcp/tree/main) | Project overview and empty source placeholders |
| [tcp](https://github.com/ST3PAN0V/file-transfer-udp-tcp/tree/tcp) | TCP client, server, and transfer test |
| [udp](https://github.com/ST3PAN0V/file-transfer-udp-tcp/tree/udp) | UDP client, server, and transfer test |

**Use the `tcp` or `udp` branch to run the programs.** Both implementation branches use this layout:

| Path | Purpose |
| --- | --- |
| `src/server.py` | Serve the file selected on the command line |
| `src/client.py` | Receive data and write it to the selected output file |
| `src/config.py` | Socket settings and buffer size; the UDP branch also defines a timeout |
| `test/test_script.sh` | Generate a test file, run the transfer, and compare contents |

## How it works

- The server opens a file in binary mode and sends it in blocks.
- The TCP client reads until the connection closes.
- The UDP client sends an initial datagram, then receives data until an inactivity timeout or an empty datagram.
- Each server handles one transfer and then exits.
- The server argument selects the source file. The client argument selects a local output path; it does not request an arbitrary pathname from the server.

The code uses Python's standard library. The test scripts use Bash and common Unix utilities, including `cmp`.

## Set up

Requirements: Git, Python 3 with `venv` support, and a Unix-like environment for the Bash tests. A virtual environment makes the `python` command used by the scripts resolve to Python 3; there are no third-party Python packages to install.

```bash
git clone --branch tcp https://github.com/ST3PAN0V/file-transfer-udp-tcp.git
cd file-transfer-udp-tcp
python3 -m venv .venv
source .venv/bin/activate
python --version
```

To try UDP in the same checkout:

```bash
git switch udp
```

Connection settings are defined in `src/config.py` on each branch. The client and server must use matching settings.

## Run a transfer

In the first terminal, from the repository root with the virtual environment active:

```bash
printf 'A small file-transfer example.\n' > sample-input.txt
python src/server.py sample-input.txt
```

Wait for the server's `serving` message. In a second terminal, open the same repository directory and run:

```bash
source .venv/bin/activate
python src/client.py sample-output.txt
cmp sample-input.txt sample-output.txt
```

`cmp` exits with status `0` when the files are identical. The client overwrites the output file if it already exists. Restart the server before each new transfer.

## Run the supplied test

On either implementation branch, from the repository root:

```bash
source .venv/bin/activate
(cd test && bash test_script.sh)
cmp test/original_test_file.txt test/received_test_file.txt
```

The script generates roughly 1–10 MiB of random alphanumeric data, waits for readiness messages in the program logs, and compares the files. Its final success message does not reliably indicate a matching transfer, so check the explicit `cmp` result above.

Logs and generated files are placed under `test/`. To remove the test artifacts:

```bash
(cd test && bash test_script.sh --clean)
```

## Implementation limits

- **TCP:** the server currently uses `send()` without checking how many bytes were written. Handling partial writes is necessary before relying on complete transfers in all conditions.
- **UDP:** there are no sequence numbers, acknowledgements, or retransmissions. Lost or reordered datagrams are not recovered, and an inactivity timeout is treated as the end of the transfer.
- **Concurrency:** the servers are designed for a single transfer per run; they do not accept concurrent clients.
- **Verification:** the test scripts provide a local exercise, not a guarantee of reliable delivery for arbitrary file sizes or network conditions.

The original assignment asked for TCP and UDP file-transfer programs and a Bash test using a file larger than 1 MiB. The implementation keeps the deliberately limited, single-client scope described by the author.
