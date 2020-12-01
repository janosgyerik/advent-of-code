package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

func readFile(p string) (nums []int, err error) {
	b, err := ioutil.ReadFile(p)
	if err != nil {
		return nil, err
	}

	lines := strings.Split(string(b), "\n")
	nums = make([]int, 0, len(lines))

	for _, line := range lines {
		// at the end of the file, when it's terminated with EOL
		if len(line) == 0 {
			continue
		}

		num, err := strconv.Atoi(line)
		if err != nil {
			return nil, err
		}
		nums = append(nums, num)
	}

	return nums, nil
}

func twoSum(nums []int, target int) (int, int, bool) {
	seen := make(map[int]bool)
	for _, b := range nums {
		a := target - b
		if _, ok := seen[a]; ok {
			return a, b, true
		}
		seen[b] = true
	}
	return 0, 0, false
}

func threeSum(nums []int, target int) (int, int, int, bool) {
	for i, a := range nums {
		for j := i + 1; j < len(nums); j++ {
			b := nums[j]
			for k := j + 1; k < len(nums); k++ {
				c := nums[k]
				if a+b+c == target {
					return a, b, c, true
				}
			}
		}
	}
	return 0, 0, 0, false
}

func main() {
	nums, err := readFile(os.Args[1])
	if err != nil {
		panic(err)
	}

	a, b, _ := twoSum(nums, 2020)
	fmt.Printf("%d * %d = %d\n", a, b, a*b)

	a, b, c, _ := threeSum(nums, 2020)
	fmt.Printf("%d * %d * %d = %d\n", a, b, c, a*b*c)
}
