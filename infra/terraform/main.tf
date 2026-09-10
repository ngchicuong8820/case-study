provider "aws" {
  region = "us-east-1"
}

# Tài nguyên mẫu để công cụ IaC Scanning (Trivy/Semgrep) quét lỗi cấu hình
resource "aws_s3_bucket" "secure_bucket" {
  bucket = "devsecops-secure-bucket-demo"

  # Cố tình tuân thủ cấu hình bảo mật (tắt public access để pass qua security gate)
  # Nếu muốn test tính năng Block của IaC, bạn có thể thử đổi thành acl = "public-read"
}

resource "aws_s3_bucket_ownership_controls" "example" {
  bucket = aws_s3_bucket.secure_bucket.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}