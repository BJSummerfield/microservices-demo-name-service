#!/usr/bin/env bash
set -e

mysql_host="$1"
mysql_port="$2"
rabbitmq_host="$3"
rabbitmq_port="$4"
shift 4

# Wait for MySQL
until nc -z "$mysql_host" "$mysql_port"; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done
>&2 echo "MySQL is up - executing command"

# Wait for RabbitMQ
until nc -z "$rabbitmq_host" "$rabbitmq_port"; do
  >&2 echo "RabbitMQ is unavailable - sleeping"
  sleep 1
done
>&2 echo "RabbitMQ is up - executing command"

exec "$@"

