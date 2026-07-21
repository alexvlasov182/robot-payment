variable "my_ip" {
  description = "Your public IP for SSH (format: 1.2.3.4/32)"
  type        = string
}

variable "key_name" {
  description = "Name of EC2 key pair (the one you created)"
  type        = string
  default     = "ec2-key"
}
