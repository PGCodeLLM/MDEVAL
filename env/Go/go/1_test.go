package main

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
)

func calculateTriangleArea(a, b, c float64) float64 {
	if a+b > c && a+c > b && b+c > a {
		s := (a + b + c) / 2.0
		area := math.Sqrt(s * (s - a) * (s - b) * (s - c))
		return math.Round(area*100) / 100
	} else {
		return -1 // Indicating it's not a triangle
	}
}

func TestCalculateTriangleArea(t *testing.T) {
	// Using a small delta for floating point comparison
	const delta = 1e-6

	assert := assert.New(t)

	// Triangle with sides 3, 5, 4 should return area 6.00
	assert.InDelta(6.00, calculateTriangleArea(3, 5, 4), delta)

	// Not a triangle with sides 1, 1, 4 should return -1
	assert.Equal(-1.0, calculateTriangleArea(1, 1, 4))

	// Triangle with sides 7, 24, 25 should return area 84.00
	assert.InDelta(84.00, calculateTriangleArea(7, 24, 25), delta)

	// Triangle with sides 10.5, 6.2, 7.3 should return close to calculated area
	assert.InDelta(22.15, calculateTriangleArea(10.5, 6.2, 7.3), 1e-2) // Looser delta for specific precision
}