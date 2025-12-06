#!/bin/bash

STARTING_PORT=${1:-${WEB_PORT:-8001}}
PORT=$STARTING_PORT
MAX_PORT=9000

echo "Checking for available port starting from $STARTING_PORT..."

is_port_in_use() {
    lsof -i :$1 > /dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ":$1 "
}

while [ $PORT -le $MAX_PORT ]; do
    if is_port_in_use $PORT; then
        echo "Port $PORT is busy, trying next port..."
        PORT=$((PORT + 1))
    else
        echo "✓ Found available port: $PORT"
        break
    fi
done

if [ $PORT -gt $MAX_PORT ]; then
    echo "ERROR: No available ports found between $STARTING_PORT and $MAX_PORT"
    exit 1
fi

if [ -f .env ]; then
    if grep -q "^WEB_PORT=" .env; then
        sed -i "s/^WEB_PORT=.*/WEB_PORT=$PORT/" .env
        echo "Updated WEB_PORT in .env to $PORT"
    else
        echo "WEB_PORT=$PORT" >> .env
        echo "Added WEB_PORT=$PORT to .env"
    fi
fi

export WEB_PORT=$PORT

echo ""
echo "Starting Docker containers with WEB_PORT=$PORT..."
echo "Access the application at: http://localhost:$PORT"
echo ""

docker-compose up -d

echo ""
echo "Container status:"
docker-compose ps
