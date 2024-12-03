BLACK := black --check .
FLAKE8 := flake8 .
VENV := venv

# Build the Docker image
.PHONY: build
build:
	docker-compose up --build -d

.PHONY: down
down:
	docker compose down

.PHONY: prune
prune:
	docker system prune -a

.PHONY: lint
lint: venv
	$(VENV)/bin/$(BLACK)
	$(VENV)/bin/$(FLAKE8)

.PHONY: format
format: venv
	$(VENV)/bin/black .

.PHONY: flake8
flake8: venv
	$(VENV)/bin/$(FLAKE8)

.PHONY: black
black: venv
	$(VENV)/bin/$(BLACK)

.PHONY: venv
venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

.PHONY: clean
clean:
	rm -rf $(VENV)

# Create DynamoDB table
.PHONY: create-dynamodb-table
create-dynamodb-table:
	@echo "Creating DynamoDB table with name: $(TABLE_NAME)"
	aws dynamodb create-table \
		--table-name $(TABLE_NAME) \
		--attribute-definitions $(ATTRIBUTE_DEFINITIONS) \
		--key-schema $(KEY_SCHEMA) \
		--provisioned-throughput $(PROVISIONED_THROUGHPUT)

# Usage: make create-dynamodb-table TABLE_NAME=my-table ATTRIBUTE_DEFINITIONS="AttributeName=Id,AttributeType=S" KEY_SCHEMA="AttributeName=Id,KeyType=HASH" PROVISIONED_THROUGHPUT="ReadCapacityUnits=5,WriteCapacityUnits=5"

# Create Lambda function
.PHONY: create-lambda-function
create-lambda-function:
	@echo "Creating Lambda function with name: $(FUNCTION_NAME)"
	aws lambda create-function \
		--function-name $(FUNCTION_NAME) \
		--runtime python3.9 \
		--role $(ROLE) \
		--handler src.lambda_function.lambda_handler \
		--zip-file fileb://$(ZIP_FILE)

# Usage: make create-lambda-function FUNCTION_NAME=my-function ROLE=arn:aws:iam::123456789012:role/execution_role ZIP_FILE=function.zip

# Create API Gateway 
.PHONY: create-api-gateway
create-api-gateway:
	@echo "Creating API Gateway with name: $(API_NAME)"
	aws apigatewayv2 create-api \
		--name $(API_NAME) \
		--protocol-type $(PROTOCOL_TYPE) \
		--target $(TARGET) \

# Usage: make create-api-gateway API_NAME=my-api API_DESCRIPTION="My API Gateway"

# Create route in API Gateway
.PHONY: create-route
create-route:
	@echo "Creating route in API Gateway with name: $(ROUTE_NAME)"
	aws apigatewayv2 create-route \
		--api-id $(API_ID) \
		--route-key $(ROUTE_KEY) \
