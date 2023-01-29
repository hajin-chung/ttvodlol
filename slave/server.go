package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net/http"
)

const ADDR = "127.0.0.1:4000"

func ping(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "pong")
}

func startDownload(w http.ResponseWriter, r *http.Request) {
	queue, _ := getQueue()
	for _, video := range queue.Videos {
		err := downloadVod(video.URL)
		if err != nil {
			notify("error", fmt.Sprintf("download %s failed", video.ID))
			continue
		}
		popQueue(video.ID)
	}
	io.WriteString(w, "hello")
}

func test(w http.ResponseWriter, r *http.Request) {
	err := downloadVod("https://usher.ttvnw.net/vod/1716923641.m3u8?sig=50861301748e0beaed36b8db38dec05e948a3c3a&token=%7B%22authorization%22%3A%7B%22forbidden%22%3Afalse%2C%22reason%22%3A%22%22%7D%2C%22chansub%22%3A%7B%22restricted_bitrates%22%3A%5B%5D%7D%2C%22device_id%22%3Anull%2C%22expires%22%3A1674996342%2C%22https_required%22%3Atrue%2C%22privileged%22%3Atrue%2C%22user_id%22%3A569530460%2C%22version%22%3A2%2C%22vod_id%22%3A1716923641%7D&allow_source=true")
	if err != nil {
		log.Printf("Error on download vod: %s", err)
		w.WriteHeader(http.StatusInternalServerError)
		return
	}
	io.WriteString(w, "test")
}

func WithContext(ctx context.Context, next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

func WithLogger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Println(r.Method, r.RequestURI)
		next.ServeHTTP(w, r)
	})
}

func startServer() {
	mux := http.NewServeMux()
	ctx := context.Background()

	// // init db
	// db, dbErr := initDB()
	// if dbErr != nil {
	// 	log.Fatalln(dbErr)
	// }
	// defer db.Close()

	// init context
	ctx = context.WithValue(ctx, "test", "hihi")
	// ctx = context.WithValue(ctx, "db", db)

	mux.HandleFunc("/ping", ping)
	mux.HandleFunc("/start", startDownload)
	mux.HandleFunc("/test", test)

	contextMux := WithLogger(WithContext(ctx, mux))
	err := http.ListenAndServe(ADDR, contextMux)
	if err != nil {
		log.Fatalln(err)
	}
}
