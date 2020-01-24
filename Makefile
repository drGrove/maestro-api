.PHONY: protos
protos:
	protoc \
	-I. \
	-I $$GOPATH/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis/ \
	--go_out=plugins=grpc:. \
	--grpc-gateway_out=logtostderr=true:. \
	proto/*.proto

.PHONY: run
run:
	GO111MODULE=on go run cmd/main.go
