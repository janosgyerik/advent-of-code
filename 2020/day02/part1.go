package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"regexp"
	"strconv"
)

var lineRegex = regexp.MustCompile(`(?P<min>\d+)-(?P<max>\d+) (?P<c>.): (?P<password>.+)`)

func parse(line string) (int, int, rune, string) {
	match := lineRegex.FindStringSubmatch(line)
	params := make(map[string]string)
	for i, name := range lineRegex.SubexpNames() {
		if 0 < i && i <= len(match) {
			params[name] = match[i]
		}
	}

	min, _ := strconv.Atoi(params["min"])
	max, _ := strconv.Atoi(params["max"])
	c := []rune(params["c"])[0]
	password := params["password"]
	return min, max, c, password
}

func isValid(line string) bool {
	min, max, c, password := parse(line)
	count := 0
	for _, c2 := range password {
		if c2 == c {
			count++
		}
	}

	return min <= count && count <= max
}

func isValid2(line string) bool {
	p1, p2, c, password := parse(line)
	c1 := []rune(password)[p1-1]
	c2 := []rune(password)[p2-1]

	return (c1 == c) != (c2 == c)
}

func main() {
	file, err := os.Open(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	count := 0
	count2 := 0
	rd := bufio.NewReader(file)
	for {
		line, err := rd.ReadString('\n')

		if err == io.EOF {
			break
		}

		if isValid(line) {
			count++
		}

		if isValid2(line) {
			count2++
		}
	}

	fmt.Println(count)
	fmt.Println(count2)
}
