package connect

import (
	"fmt"
)

func PostgresURI() string {
	connStr := fmt.Sprintf(
		"postgres://%s:%s@%s/%s?sslmode=disable",
		getEnv("POSTGRES_USER", "postgres"),
		getEnv("POSTGRES_PASSWORD", "postgres"),
		getEnv("POSTGRES_HOST", "postgres"),
		getEnv("POSTGRES_DATABASE", "hawkeye"),
	)
	return connStr
}
