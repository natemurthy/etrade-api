package main

import (
	"bufio"
	"fmt"
	"log"
	"net/url"
	"os"
	"strings"

	"github.com/dghubble/oauth1"
	"github.com/pkg/browser"
)

var (
	consumerKey    = os.Getenv("CONSUMER_KEY")
	consumerSecret = os.Getenv("CONSUMER_SECRET")
)

// GenerateAuthURL derived from config.AuthorizationURL but slightly tuned
// to fit the shape of the Etrade API
func GenerateAuthURL(token, key, baseAuthURL string) (*url.URL, error) {
	authorizationURL, err := url.Parse(baseAuthURL)
	if err != nil {
		return nil, err
	}
	values := authorizationURL.Query()
	values.Add("key", key)
	values.Add("token", token)
	authorizationURL.RawQuery = values.Encode()
	return authorizationURL, nil
}

func main() {
	var endpoint oauth1.Endpoint

	endpoint.RequestTokenURL = "https://api.etrade.com/oauth/request_token"
	endpoint.AuthorizeURL = "https://us.etrade.com/e/t/etws/authorize"
	endpoint.AccessTokenURL = "https://api.etrade.com/oauth/access_token"

	config := oauth1.NewConfig(consumerKey, consumerSecret)
	config.Endpoint = endpoint
	config.CallbackURL = "oob"

	requestToken, requestTokenSecret, err := config.RequestToken()
	if err != nil {
		log.Fatal(err)
	}

	//fmt.Println(requestToken)
	//fmt.Println(requestTokenSecret)

	authURL, err := GenerateAuthURL(requestToken, consumerKey, endpoint.AuthorizeURL)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Opening browser, navigating to", authURL.String())
	browser.OpenURL(authURL.String())

	fmt.Print("Enter oauth_verifier: ")
	reader := bufio.NewReader(os.Stdin)
	verifierCode, err := reader.ReadString('\n')
	if err != nil {
		log.Fatalf("An error occurred while reading input. Please try again: %v", err)
	}
	verifierCode = strings.TrimSuffix(verifierCode, "\n")

	accessToken, accessSecret, err := config.AccessToken(requestToken, requestTokenSecret, verifierCode)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(accessToken)
	fmt.Println(accessSecret)

}
