package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec"
)

var hwcMainFilePath *string = flag.String("hwcmain", "./main.py", "Main python file of hardware controller")
var help bool = *flag.Bool("help", false, "help lol")
var addr *string = flag.String("addr", "0.0.0.0:80", "bind addr")

var hwcInstance *exec.Cmd

func init() {
	flag.Parse() // Parse flags (arguments)
}

func main() {
	go signalCatcher()
	hwcInstance = exec.Command(*hwcMainFilePath)
	if help {
		printHelp()
		exit(0)
	}
	fmt.Println("The RoboArm http api server is starting up...")
	_, err := os.Stat(*hwcMainFilePath)
	if err != nil {
		fmt.Println("Error: Could not find main.py file of hardware controller!")
		printHelp()
		if !isDebugMode() {
			exit(2)
		}
	}
	serverMain()
}

func printHelp() {
	fmt.Print(`Usage: roboarm-httpserver [flags]
	
	Available flags:
		--help		- show help
		--hwcmain	- specify path for main.py of hardware controller
		--addr		- address:port to bind to (use 0.0.0.0 or just :port for all interfaces)`)
	fmt.Println()
}

func isDebugMode() bool {
	if os.Getenv("HTTPSRV_DEBUG") == "1" {
		return true
	} else {
		return false
	}
}

func printDebug(msg any) {
	if isDebugMode() {
		fmt.Println("[DEBUG]", msg)
	}
}
