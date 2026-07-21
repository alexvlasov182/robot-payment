provider "aws" {
  region = "eu-central-1" # Change if needed
}

data "aws_ami" "ubuntu" {
  most_recent = true
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
  owners = ["099720109477"]
}

resource "aws_security_group" "api_sg" {
  name        = "fastapi-security-group"
  description = "Allow SSH from my IP, HTTP from anywhere"

  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip] # <-- YOUR IP GOES HERE
  }

  ingress {
    description = "HTTP (nginx)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "ec2_ssm_role" {
  name = "FastAPISSMReadRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "ec2.amazonaws.com" }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "FastAPIInstanceProfile"
  role = aws_iam_role.ec2_ssm_role.name
}

resource "aws_instance" "api_server" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = "t3.micro"
  security_groups      = [aws_security_group.api_sg.name]
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
  key_name             = var.key_name

  user_data = <<-EOF
    #!/bin/bash
    set -e
    apt-get update -y
    apt-get install -y docker.io docker-compose-v2 awscli jq

    systemctl enable docker
    systemctl start docker

    curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | bash
    apt-get install -y gitlab-runner

    usermod -aG docker gitlab-runner

    mkdir -p /home/gitlab-runner/app
    chown -R gitlab-runner:gitlab-runner /home/gitlab-runner/app

    systemctl enable gitlab-runner
    systemctl restart gitlab-runner
  EOF

  tags = {
    Name = "RobotPaymentAPI"
  }
}

output "server_public_ip" {
  value = aws_instance.api_server.public_ip
}

output "ssh_command" {
  value = "ssh -i ~/.ssh/ec2-key.pem ubuntu@${aws_instance.api_server.public_ip}"
}
