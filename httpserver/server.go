package main

import (
	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
)

func serverMain() {
	router := gin.Default()
	router.Use(static.Serve("/", static.LocalFile("static", false)))

	router.GET("/api/v1/sys", sysCmdHandler)
	router.Run(*addr)
}
