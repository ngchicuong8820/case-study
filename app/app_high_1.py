def get_cloud_credentials():
    # Lỗ hổng High: Lộ thông tin khóa bảo mật (Hardcoded AWS Keys)
    aws_access_key = "AKIAIOSFODNN7EXAMPLE"
    aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    return aws_access_key, aws_secret_key