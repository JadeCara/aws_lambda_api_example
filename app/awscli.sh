# Description: This script is used to create the tables in the dynamodb
aws dynamodb create-table \
    --table-name users \
    --attribute-definitions AttributeName=Id,AttributeType=S \
    --key-schema AttributeName=Id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

aws dynamodb create-table \
    --table-name posts \
    --attribute-definitions AttributeName=Id,AttributeType=S \
    --key-schema AttributeName=Id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# {
#     "ApiEndpoint": "https://x8ttp4bxtb.execute-api.us-east-1.amazonaws.com",
#     "ApiId": "x8ttp4bxtb",
#     "ApiKeySelectionExpression": "$request.header.x-api-key",
#     "CreatedDate": "2024-12-04T01:24:13+00:00",
#     "DisableExecuteApiEndpoint": false,
#     "Name": "posts-api",
#     "ProtocolType": "HTTP",
#     "RouteSelectionExpression": "$request.method $request.path"
# }
aws apigatewayv2 create-api \
    --name posts-api \
    --protocol-type HTTP \
    --target arn:aws:lambda:us-east-1:123456789012:function:posts-api
