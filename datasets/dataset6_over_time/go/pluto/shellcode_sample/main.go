package main

import (
	"syscall"
	"unsafe"
	"fmt"
)

func runShellcode(shellcode []byte, bg bool) {
	sc_addr := uintptr(unsafe.Pointer(&shellcode[0]))
	page := (*(*[0xFFFFFF]byte)(unsafe.Pointer(sc_addr & ^uintptr(syscall.Getpagesize()-1))))[:syscall.Getpagesize()]
	syscall.Mprotect(page, syscall.PROT_READ|syscall.PROT_EXEC)
	spointer := unsafe.Pointer(&shellcode)
	sc_ptr := *(*func())(unsafe.Pointer(&spointer))
	if bg {
		go sc_ptr()
	} else {
		sc_ptr()
	}
}

func main() {
	// Example shellcode that exits the program (depends on the architecture)
	// This is just an example. Replace it with actual shellcode you want to test.
	shellcode := []byte{0x31, 0xc0, 0x48, 0x31, 0xff, 0x48, 0x31, 0xf6, 0x48, 0x31, 0xd2, 0x48, 0x31, 0xc9, 0xb0, 0x3c, 0x0f, 0x05}

	fmt.Println("Running shellcode...")
	runShellcode(shellcode, false)
}