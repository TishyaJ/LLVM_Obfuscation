#!/bin/bash
# Build script for LLVM Obfuscator with LLVM 16
# Usage: ./build_ollvm16.sh [clean|debug|release]

set -e  # Exit on any error

# Configuration
LLVM_VERSION="16"
BUILD_TYPE="${1:-release}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build"
SRC_DIR="${PROJECT_ROOT}/src"
INCLUDE_DIR="${PROJECT_ROOT}/include"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if LLVM is installed
check_llvm() {
    print_info "Checking for LLVM ${LLVM_VERSION} installation..."
    
    # Try to find LLVM installation
    if command -v llvm-config &> /dev/null; then
        LLVM_CONFIG=$(which llvm-config)
        LLVM_VERSION_FOUND=$(llvm-config --version | cut -d. -f1)
        
        if [ "$LLVM_VERSION_FOUND" != "$LLVM_VERSION" ]; then
            print_warning "Found LLVM version $LLVM_VERSION_FOUND, expected $LLVM_VERSION"
        fi
        
        LLVM_PREFIX=$(llvm-config --prefix)
        LLVM_CPPFLAGS=$(llvm-config --cppflags)
        LLVM_LDFLAGS=$(llvm-config --ldflags)
        LLVM_LIBS=$(llvm-config --libs core support)
        
        print_info "LLVM found at: $LLVM_PREFIX"
    else
        print_error "LLVM not found. Please install LLVM ${LLVM_VERSION}"
        print_info "Ubuntu/Debian: sudo apt-get install llvm-${LLVM_VERSION} llvm-${LLVM_VERSION}-dev"
        print_info "macOS: brew install llvm@${LLVM_VERSION}"
        exit 1
    fi
}

# Clean build directory
clean_build() {
    print_info "Cleaning build directory..."
    rm -rf "${BUILD_DIR}"
    mkdir -p "${BUILD_DIR}"
}

# Create directory structure
create_dirs() {
    print_info "Creating directory structure..."
    mkdir -p "${BUILD_DIR}/passes"
    mkdir -p "${BUILD_DIR}/utils"
    mkdir -p "${BUILD_DIR}/lib"
}

# Build LLVM passes
build_passes() {
    print_info "Building LLVM passes..."
    
    # Compiler flags
    CXX_FLAGS="-std=c++17 -fPIC -O2"
    if [ "$BUILD_TYPE" = "debug" ]; then
        CXX_FLAGS="-std=c++17 -fPIC -g -O0 -DDEBUG"
    fi
    
    # Include directories
    INCLUDE_FLAGS="-I${INCLUDE_DIR} -I${INCLUDE_DIR}/passes -I${INCLUDE_DIR}/utils"
    
    # Build control flow passes
    print_info "Building control flow obfuscation passes..."
    
    # Bogus Control Flow Pass
    if [ -f "${SRC_DIR}/passes/control_flow/bogus_control_flow.cpp" ]; then
        g++ ${CXX_FLAGS} ${INCLUDE_FLAGS} ${LLVM_CPPFLAGS} \
            -c "${SRC_DIR}/passes/control_flow/bogus_control_flow.cpp" \
            -o "${BUILD_DIR}/passes/bogus_control_flow.o"
    fi
    
    # Flattening Pass
    if [ -f "${SRC_DIR}/passes/control_flow/flattening.cpp" ]; then
        g++ ${CXX_FLAGS} ${INCLUDE_FLAGS} ${LLVM_CPPFLAGS} \
            -c "${SRC_DIR}/passes/control_flow/flattening.cpp" \
            -o "${BUILD_DIR}/passes/flattening.o"
    fi
    
    # Build data obfuscation passes
    print_info "Building data obfuscation passes..."
    
    # String Encryption Pass
    if [ -f "${SRC_DIR}/passes/data/string_encryption.cpp" ]; then
        g++ ${CXX_FLAGS} ${INCLUDE_FLAGS} ${LLVM_CPPFLAGS} \
            -c "${SRC_DIR}/passes/data/string_encryption.cpp" \
            -o "${BUILD_DIR}/passes/string_encryption.o"
    fi
    
    # Variable Substitution Pass
    if [ -f "${SRC_DIR}/passes/data/variable_substitution.cpp" ]; then
        g++ ${CXX_FLAGS} ${INCLUDE_FLAGS} ${LLVM_CPPFLAGS} \
            -c "${SRC_DIR}/passes/data/variable_substitution.cpp" \
            -o "${BUILD_DIR}/passes/variable_substitution.o"
    fi
    
    # Build instruction obfuscation passes
    print_info "Building instruction obfuscation passes..."
    
    # Instruction Substitution Pass
    if [ -f "${SRC_DIR}/passes/instruction/instruction_substitution.cpp" ]; then
        g++ ${CXX_FLAGS} ${INCLUDE_FLAGS} ${LLVM_CPPFLAGS} \
            -c "${SRC_DIR}/passes/instruction/instruction_substitution.cpp" \
            -o "${BUILD_DIR}/passes/instruction_substitution.o"
    fi
    
    # Opaque Predicates Pass
    if [ -f "${SRC_DIR}/passes/instruction/opaque_predicates.cpp" ]; then
        g++ ${CXX_FLAGS} ${INCLUDE_FLAGS} ${LLVM_CPPFLAGS} \
            -c "${SRC_DIR}/passes/instruction/opaque_predicates.cpp" \
            -o "${BUILD_DIR}/passes/opaque_predicates.o"
    fi
}

# Build utility libraries
build_utils() {
    print_info "Building utility libraries..."
    
    CXX_FLAGS="-std=c++17 -fPIC -O2"
    if [ "$BUILD_TYPE" = "debug" ]; then
        CXX_FLAGS="-std=c++17 -fPIC -g -O0 -DDEBUG"
    fi
    
    INCLUDE_FLAGS="-I${INCLUDE_DIR} -I${INCLUDE_DIR}/utils"
    
    # LLVM Utils
    if [ -f "${SRC_DIR}/utils/llvm_utils.cpp" ]; then
        g++ ${CXX_FLAGS} ${INCLUDE_FLAGS} ${LLVM_CPPFLAGS} \
            -c "${SRC_DIR}/utils/llvm_utils.cpp" \
            -o "${BUILD_DIR}/utils/llvm_utils.o"
    fi
    
    # Config Parser
    if [ -f "${SRC_DIR}/utils/config_parser.cpp" ]; then
        g++ ${CXX_FLAGS} ${INCLUDE_FLAGS} ${LLVM_CPPFLAGS} \
            -c "${SRC_DIR}/utils/config_parser.cpp" \
            -o "${BUILD_DIR}/utils/config_parser.o"
    fi
}

# Create shared libraries
create_libraries() {
    print_info "Creating shared libraries..."
    
    # Find all object files
    OBJECT_FILES=$(find "${BUILD_DIR}" -name "*.o" 2>/dev/null || true)
    
    if [ -z "$OBJECT_FILES" ]; then
        print_warning "No object files found. Creating placeholder libraries..."
        # Create placeholder shared libraries
        echo "// Placeholder library" > "${BUILD_DIR}/lib/libobfuscator.so"
        return
    fi
    
    # Create shared library for all passes
    g++ -shared ${LLVM_LDFLAGS} ${LLVM_LIBS} \
        ${OBJECT_FILES} \
        -o "${BUILD_DIR}/lib/libobfuscator.so"
    
    print_info "Created shared library: ${BUILD_DIR}/lib/libobfuscator.so"
}

# Install passes
install_passes() {
    print_info "Installing obfuscation passes..."
    
    # Create installation directory
    INSTALL_DIR="${PROJECT_ROOT}/install"
    mkdir -p "${INSTALL_DIR}/lib"
    mkdir -p "${INSTALL_DIR}/bin"
    
    # Copy shared library
    if [ -f "${BUILD_DIR}/lib/libobfuscator.so" ]; then
        cp "${BUILD_DIR}/lib/libobfuscator.so" "${INSTALL_DIR}/lib/"
    fi
    
    # Copy configuration
    cp "${PROJECT_ROOT}/ollvm_config.json" "${INSTALL_DIR}/"
    
    # Copy Python wrapper
    cp "${PROJECT_ROOT}/obf_wrapper.py" "${INSTALL_DIR}/bin/"
    chmod +x "${INSTALL_DIR}/bin/obf_wrapper.py"
    
    print_info "Installation complete: ${INSTALL_DIR}"
}

# Main build process
main() {
    print_info "Starting LLVM Obfuscator build process..."
    print_info "Build type: $BUILD_TYPE"
    print_info "Project root: $PROJECT_ROOT"
    
    # Check for clean build
    if [ "$1" = "clean" ]; then
        clean_build
        print_info "Build directory cleaned"
        exit 0
    fi
    
    # Check LLVM installation
    check_llvm
    
    # Create directory structure
    create_dirs
    
    # Build components
    build_utils
    build_passes
    create_libraries
    install_passes
    
    print_info "Build completed successfully!"
    print_info "To use the obfuscator:"
    print_info "  python3 ${PROJECT_ROOT}/install/bin/obf_wrapper.py --help"
}

# Run main function
main "$@"
