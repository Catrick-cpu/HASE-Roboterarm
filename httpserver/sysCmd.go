package main

import (
	"net/http"
	"os/exec"

	"github.com/gin-gonic/gin"
)

func sysCmdHandler(c *gin.Context) {
	reqCmd, _ := c.GetQuery("cmd")
	printDebug(c.Request.RequestURI)
	var execErr string = ""
	switch reqCmd {
	case "poweroff":
		execErr = exec.Command("/usr/bin/poweroff").Run().Error()
	case "reboot":
		execErr = exec.Command("/usr/bin/reboot").Run().Error()
	case "verify":
		execErr = exec.Command("/usr/bin/wall", "Test").Run().Error()
	default:
		execErr = "nf"
	}
	if len(execErr) == 0 {
		c.Data(http.StatusOK, gin.MIMEPlain, []byte("OK!"))
	}
	if execErr == "nf" {
		c.Data(http.StatusNotFound, gin.MIMEPlain, []byte("Not found"))
	}
	if execErr != "" {
		printDebug(execErr)
		c.Data(http.StatusInternalServerError, gin.MIMEPlain, []byte(execErr))
	} else {
		c.Data(http.StatusOK, gin.MIMEPlain, []byte("OK!"))
	}
}
