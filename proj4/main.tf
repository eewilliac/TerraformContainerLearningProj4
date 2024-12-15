terraform {
    required_providers {
        docker = {
            source  = "kreuzwerker/docker"
            version = "3.0.2"
        }
    }
}

provider "docker" {}

resource "docker_network" "devnet" {
  name   = "devnet"
  driver = "bridge"
}

resource "docker_volume" "db_data" {
  name = "db_data"
}

resource "docker_container" "mysqldb" {
  name  = "mysqldb"
  image = "mysql:latest"
  
  ports {
    internal = 3306
    external = 3306
  }

  networks_advanced {
    name = docker_network.devnet.name
  }

  env = [
    "MYSQL_ROOT_PASSWORD=quimica"
  ]

  # Host-mounted volume for SQL scripts
  volumes {
    host_path      = "/home/ewc/code/TerraformAndDocker/proj4/db_files"  # Ensure this is an absolute path
    container_path = "/docker-entrypoint-initdb.d"
  }

  # Docker-managed named volume for MySQL data
  volumes {
    volume_name    = docker_volume.db_data.name  # Use 'volume_name' for named volumes
    container_path = "/var/lib/mysql"
  }
}

resource "docker_image" "mypy_image" {
  name         = "mypy:latest"
  build {
    context    = "${path.module}"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "mypy" {
  name  = "mypy_container"
  image = docker_image.mypy_image.name

  ports {
    internal = 5000
    external = 8080
  }

  networks_advanced {
    name = docker_network.devnet.name
  }

  depends_on = [docker_container.mysqldb]

  command = ["python3", "app.py"]
}