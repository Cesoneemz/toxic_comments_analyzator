FROM golang:1.22-alpine

WORKDIR /app

COPY . .

RUN go build main.go

CMD ["./main"]