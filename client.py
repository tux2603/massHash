from hashlib import md5
import sys
import socket

maxZeros = 0

if __name__ == '__main__':
    word = input().lower()
    print(sys.argv)

    if len(sys.argv) < 5:
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    start = int(sys.argv[3])
    stride = int(sys.argv[4])

    maxNum = sys.argv[5] if len(sys.argv) > 5 else 655536

    while word is not None:

        for num in range(start, maxNum, stride):
            code = f'{word}{int(num):d}'
            hashStr = md5(code.encode('utf-8')).hexdigest()
            # print(code, end=': ')
            # print(md5(code.encode('utf-8')).hexdigest())

            for i in range(32):
                if hashStr[i] != '0':
                    if i >= maxZeros:

                        if i > maxZeros:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.connect((host, port))
                                s.sendall(f'z{i}'.encode('utf-8'))
                                maxZeros = max(int(s.recv(64).decode('utf-8')), i)

                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((host, port))
                            s.sendall(f'k{i} {code} {hashStr}'.encode('utf-8'))
                            maxZeros = max(int(s.recv(64).decode('utf-8')), i)

                        # print(code, end=': ')
                        # print(hashStr)

                    break

        word = input().lower()
