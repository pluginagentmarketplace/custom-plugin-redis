#!/bin/bash
# Redis Installation Script
# Supports: Ubuntu/Debian, RHEL/CentOS, macOS

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    elif [ -f /etc/redhat-release ]; then
        echo "rhel"
    else
        echo "unknown"
    fi
}

install_debian() {
    log_info "Installing Redis on Debian/Ubuntu..."
    sudo apt update
    sudo apt install -y redis-server
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
}

install_rhel() {
    log_info "Installing Redis on RHEL/CentOS..."
    sudo yum install -y epel-release
    sudo yum install -y redis
    sudo systemctl start redis
    sudo systemctl enable redis
}

install_macos() {
    log_info "Installing Redis on macOS..."
    if ! command -v brew &> /dev/null; then
        log_error "Homebrew is required. Install from https://brew.sh"
        exit 1
    fi
    brew install redis
    brew services start redis
}

verify_installation() {
    log_info "Verifying Redis installation..."

    if redis-cli ping | grep -q "PONG"; then
        log_info "Redis is running successfully!"
        redis-cli INFO server | grep redis_version
        return 0
    else
        log_error "Redis verification failed"
        return 1
    fi
}

main() {
    log_info "Starting Redis installation..."

    OS=$(detect_os)
    log_info "Detected OS: $OS"

    case $OS in
        debian)
            install_debian
            ;;
        rhel)
            install_rhel
            ;;
        macos)
            install_macos
            ;;
        *)
            log_error "Unsupported OS. Please install manually."
            exit 1
            ;;
    esac

    sleep 2
    verify_installation

    log_info "Redis installation completed!"
}

main "$@"
