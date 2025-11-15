package main

import (
	"fmt"
	"os"
	"os/signal"
	"reflect"
	"syscall"
	"time"
)

func signalCatcher() { //handle ctrl+c, systemctl stop, poweroff, etc.
	c := make(chan os.Signal, 1)
	for {
		signal.Notify(c)
		switch <-c {
		case os.Interrupt, os.Kill, syscall.SIGABRT, syscall.SIGHUP: //sighup is when loosing terminal (not wanted)
			go exit(5)
		case syscall.SIGPIPE: //Handle sigpipe
			fmt.Println("Caught SIGPIPE!")
			go exit(4)
		}
	}
}

func exit(code int) { //call this instead of os.Exit!
	if reflect.ValueOf(hwcInstance).IsZero() {
		if hwcInstance.Process.Signal(syscall.Signal(0)) == nil { //if hardware controller is running, kill it!
			fmt.Println("hardware controller is closing...")
			hwcInstance.Process.Signal(os.Interrupt)
			hwcInstance.Process.Release()
		}
	}
	time.Sleep(time.Millisecond)
	os.Exit(code)
}
