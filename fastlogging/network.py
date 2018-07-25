# -*- coding: utf-8 -*-
# Copyright 2018 Martin Bammer. All Rights Reserved.
# Licensed under MIT license.

"""Network logging support."""

import struct
import socket
from collections import deque
from threading import Thread, Event, Lock

import msgpack


class LoggingServer(Thread):

    def __init__(self, logger, address, port, maxMsgSize = 1024,
                 cbAccept = None, cbAuth = None, cbDecode = None):
        super(LoggingServer, self).__init__(name="LoggingServer_%s:%d" % (address, port), daemon=True)
        self.logger = logger
        self.address = address
        self.port = port
        self.maxMsgSize = maxMsgSize
        self.cbAccept = cbAccept
        self.cbAuth = cbAuth
        self.cbDecode = cbDecode
        self.error = None
        self.__socket = None
        self.__clients = {}
        self.__lock = Lock()
        self.__running = True
        print("LoggingServer __init__")

    def __del__(self):
        self.stop()
        print("LoggingServer __del__")

    def stop(self):
        print("STOP")
        self.__running = False
        if not self.__socket is None:
            self.__socket.close()
        self.join()

    def run(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__socket.bind((self.address, self.port))
            self.__socket.listen()
            while self.__running:
                print("WAIT ACC")
                client, (address, port) = self.__socket.accept()
                print("ACC", client, address)
                if self.cbAccept is not None and not self.cbAccept(client, address):
                    client.close()
                    continue
                print("==")
                thrClient = Thread(target=self.receiver, args=(client, address),
                                   name="LoggingReceiver%s" % address, daemon=True)
                thrClient.start()
                print("STARTED")
                with self.__lock:
                    self.__clients[client] = thrClient
        except Exception as exc:
            import traceback
            traceback.print_exc()
            self.error = exc
        for client, thrClient in tuple(self.__clients.items()):
            client.close()
            thrClient.join()
        self.__clients.clear()

    def receiver(self, client, addr):
        print("RECV", client, addr)
        try:
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except (OSError, NameError):
            pass
        client_recv = client.recv
        if self.cbAuth is None or self.cbAuth(client, addr, client_recv(self.maxMsgSize)):
            print("###")
            try:
                prefix = socket.gethostbyaddr(addr)[0] + ": "
            except:
                prefix = addr + ": "
            with client:
                logMessage = self.logger._logMessage
                msgpack_unpackb = msgpack.unpackb
                try:
                    while self.__running:
                        data = client_recv(self.maxMsgSize)
                        dataLen = len(data)
                        size = struct.unpack(">H", data)
                        print(size)
                        try:
                            if self.cbDecode is None:
                                logtime, domain, level, message, kwargs = msgpack_unpackb(data, use_list = False)
                                logMessage(None, (logtime, str(domain, "utf-8"), level, prefix + str(message, "utf-8"), kwargs), 0)
                            else:
                                logMessage(None, self.cbDecode(prefix, data), 0)
                        except:
                            print(data)
                            raise
                except Exception as exc:
                    print(exc)
                    self.error = exc
        with self.__lock:
            del self.__clients[client]


class LoggingClient(Thread):

    def __init__(self, address, port, cbConnect = None, cbEncode = None):
        super(LoggingClient, self).__init__(name="LoggingClient_%s:%d" % (address, port), daemon=True)
        self.address = address
        self.port = port
        self.queue = deque()
        self.evtQueue = Event()
        self.cbConnect = cbConnect
        self.cbEncode = cbEncode
        self.error = None
        self.__running = True
        self.__socket = None
        print("LoggingClient __init__")

    def __del__(self):
        self.stop()
        print("LoggingClient __del__")

    def stop(self):
        print("STOO")
        self.__running = False
        self.__socket.close()
        self.evtQueue.set()
        self.join()

    def log(self, entry):
        print("LOG", entry)
        self.queue.append(entry)
        self.evtQueue.set()

    def run(self):
        print("RUN")
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except (OSError, NameError):
            pass
        try:
            self.__socket.connect((self.address, self.port))
            if self.cbConnect is not None:
                if not self.cbConnect(self.__socket):
                    raise Exception("Failed to connect to %s:%d!" % (self.address, self.port))
            queue_popleft = self.queue.popleft
            sock_sendall = self.__socket.sendall
            while self.__running:
                buf = []
                try:
                    while True:
                        if self.cbEncode is None:
                            data = msgpack.packb(queue_popleft(), use_bin_type = True)
                        else:
                            data = self.cbEncode(queue_popleft())
                        buf.append(struct.pack(">H", len(data)) + data)
                except Exception as exc:
                    print(exc)
                    sock_sendall(b"".join(buf))
                    self.evtQueue.wait()
                    self.evtQueue.clear()
                    continue
        except Exception as exc:
            print(exc)
            self.error = exc
        self.__socket.close()
        print("STOPPED")
