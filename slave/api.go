package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

const ENDPOINT = "http://worker.southcoast.workers.dev"

func get(url string) (*http.Response, error) {
	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		fmt.Printf("get: could not create request to %s : %s\n", url, err)
		return nil, err
	}

	log.Printf("GET %s\n", url)
	res, err := http.DefaultClient.Do(req)

	//---test---
	// bodyBytes, bodyErr := io.ReadAll(res.Body)
	// if bodyErr != nil {
	// 	log.Fatal(bodyErr)
	// }

	// bodyString := string(bodyBytes)
	// fmt.Println(bodyString)
	//----------

	return res, err
}

func post(url string) (*http.Response, error) {
	req, err := http.NewRequest(http.MethodPost, url, nil)
	if err != nil {
		fmt.Printf("get: could not create request to %s : %s\n", url, err)
		return nil, err
	}

	log.Printf("POST %s\n", url)
	res, err := http.DefaultClient.Do(req)
	return res, err
}

func getJson(url string, target interface{}) error {
	res, err := get(url)
	if err != nil {
		log.Printf("getJson: got error from get %s : %s\n", url, err)
		return err
	}
	defer res.Body.Close()

	return json.NewDecoder(res.Body).Decode(target)
}

type Video struct {
	ID        string    `json:"id"`
	URL       string    `json:"url"`
	CreatedAt time.Time `json:"created_at"`
}

type Queue struct {
	Videos []Video `json:"videos"`
}

func getQueue() (*Queue, error) {
	queue := new(Queue)
	err := getJson(fmt.Sprintf("%s/queue", ENDPOINT), queue)
	if err != nil {
		fmt.Printf("getQueue: cannot get queue from api %s\n", err)
	}
	return queue, err
}

func popQueue(id string) error {
	_, err := post(fmt.Sprintf("%s/queue/flag/%s", ENDPOINT, id))
	if err != nil {
		fmt.Printf("popQueue: cannot pop video %s from api %s\n", id, err)
	}
	return err
}
