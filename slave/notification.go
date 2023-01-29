package main

import (
	"gopkg.in/toast.v1"
)

// sends notification
func notify(Title string, Message string) error {
	notification := toast.Notification{
		AppID:   "ttvodlol downloader",
		Title:   Title,
		Message: Message,
		Audio:   toast.Silent,
	}

	return notification.Push()
}
