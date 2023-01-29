package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"

	"github.com/grafov/m3u8"
)

// downloads segment to ./temp/{id}.ts
func downloadSegment(id string, uri string) error {
	log.Printf("downloading segment %s\n", id)
	res, err := http.Get(uri)
	if err != nil {
		return err
	}
	defer res.Body.Close()

	vodPath := fmt.Sprintf("./.temp/%s.ts", id)
	if _, err := os.Stat(vodPath); os.IsNotExist(err) {
		os.MkdirAll("./.temp", 0700) // Create your file
	}

	out, err := os.Create(vodPath)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, res.Body)
	return err
}

func downloadVod(videoUrl string) error {
	log.Printf("start downloading %s\n", videoUrl)
	res, err := get(videoUrl)
	if err != nil {
		return err
	}

	playlist, listType, err := m3u8.DecodeFrom(res.Body, true)
	if err != nil {
		return err
	}
	res.Body.Close()
	if listType != m3u8.MASTER {
		return fmt.Errorf("m3u8 type is not MASTER")
	}

	mpl := playlist.(*m3u8.MasterPlaylist)
	if len(mpl.Variants) == 0 {
		return fmt.Errorf("m3u8 playlist has no variants")
	}

	var targetUri string
	var maxBandwidth uint32 = 0
	for _, variant := range mpl.Variants {
		if variant.Bandwidth > maxBandwidth {
			maxBandwidth = variant.Bandwidth
			targetUri = variant.URI
		}
	}
	log.Printf("max bandwidth media uri: %s", targetUri)

	res, err = get(targetUri)
	if err != nil {
		return nil
	}

	playlist, listType, err = m3u8.DecodeFrom(res.Body, true)
	if err != nil {
		return err
	}
	res.Body.Close()
	if listType != m3u8.MEDIA {
		return fmt.Errorf("target uri playlist type is not MEDIA")
	}

	mediaPL := playlist.(*m3u8.MediaPlaylist)
	if len(mediaPL.Segments) == 0 {
		return fmt.Errorf("target playlist has no segments")
	}

	parsedTargetUri, err := url.Parse(targetUri)
	if err != nil {
		log.Printf("target uri parse error: %s", err.Error())
		return err
	}

	// download all segments into ./.temp
	log.Printf("media playlist segment count: %d", mediaPL.Count())
	for id := uint(0); id < mediaPL.Count(); id++ {
		segment := mediaPL.Segments[id]
		ref, err := url.Parse(segment.URI)
		if err != nil {
			log.Printf("segment uri parse error: %s", err.Error())
			continue
		}

		uri := parsedTargetUri.ResolveReference(ref)
		err = downloadSegment(fmt.Sprintf("%d", id), uri.String())
		if err != nil {
			log.Printf("download segment error: %s", err.Error())
		}
	}

	// combine all ts files in ./.temp

	return nil
}
