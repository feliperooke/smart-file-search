output "invoke_url" {
  value = "${aws_apigatewayv2_api.api.api_endpoint}/${aws_apigatewayv2_stage.dev.name}/"
}

output "s3_bucket_name" {
  value = aws_s3_bucket.file_storage.id
}
