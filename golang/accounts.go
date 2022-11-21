package main

import (
	"fmt"
	"io/ioutil"
	"os"

	"github.com/dghubble/oauth1"
)

var (
	consumerKey    = os.Getenv("CONSUMER_KEY")
	consumerSecret = os.Getenv("CONSUMER_SECRET")
	token          = os.Getenv("ACCESS_TOKEN")
	tokenSecret    = os.Getenv("TOKEN_SECRET")
)

func main() {
	config := oauth1.NewConfig(consumerKey, consumerSecret)
	token := oauth1.NewToken(token, tokenSecret)

	httpClient := config.Client(oauth1.NoContext, token)

	path := "https://api.etrade.com/v1/accounts/list.json"
	resp, _ := httpClient.Get(path)
	fmt.Println(resp.Request.URL.String())
	fmt.Println(resp.Request.Header)
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Printf("Raw Response Body:\n%v\n", string(body))
}
