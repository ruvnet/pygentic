#!/bin/bash

# Function to display the main menu
show_menu() {
    clear
    echo "***********************************"
    echo "*        PyPI Package Manager     *"
    echo "***********************************"
    echo "1. Clean old distributions"
    echo "2. Build new distributions"
    echo "3. Upload distributions to PyPI"
    echo "4. Increment version number (patch)"
    echo "5. Increment version number (minor)"
    echo "6. Increment version number (major)"
    echo "7. Advanced options"
    echo "8. Exit"
}

# Function to display the advanced menu
show_advanced_menu() {
    clear
    echo "***********************************"
    echo "*        Advanced Options         *"
    echo "***********************************"
    echo "1. Create/update .github workflow"
    echo "2. Run tests using Pytest"
    echo "3. Lint and format code"
    echo "4. Check and update dependencies"
    echo "5. Back to main menu"
}

# Function to clean old distributions
clean_dists() {
    rm -rf dist/*
    echo "🗑️  Old distributions cleaned."
}

# Function to build new distributions
build_dists() {
    python setup.py sdist bdist_wheel
    echo "📦 New distributions built."
}

# Function to upload distributions to PyPI
upload_dists() {
    twine upload dist/*
    echo "🚀 Distributions uploaded to PyPI."
}

# Function to increment version number
increment_version() {
    part=$1
    version=$(grep "version=" setup.py | sed -E "s/.*version='([0-9]+\.[0-9]+\.[0-9]+)'.*/\1/")
    IFS='.' read -r -a version_parts <<< "$version"

    if [ "$part" == "patch" ]; then
        version_parts[2]=$((version_parts[2]+1))
    elif [ "$part" == "minor" ]; then
        version_parts[1]=$((version_parts[1]+1))
        version_parts[2]=0
    elif [ "$part" == "major" ]; then
        version_parts[0]=$((version_parts[0]+1))
        version_parts[1]=0
        version_parts[2]=0
    fi

    new_version="${version_parts[0]}.${version_parts[1]}.${version_parts[2]}"
    sed -i "s/version='[0-9]\+\.[0-9]\+\.[0-9]\+'/version='$new_version'/" setup.py
    echo "🔢 Version incremented to $new_version."
}

# Function to check if required Python packages are installed
check_packages() {
    echo "🔍 Checking required Python packages..."
    required_packages=("twine" "setuptools" "wheel" "flake8" "black" "pytest" "pip-upgrader")
    for package in "${required_packages[@]}"; do
        if ! pip show "$package" > /dev/null 2>&1; then
            echo "⚠️  Package $package is not installed. Installing..."
            pip install "$package"
            echo "✅ Package $package installed."
        else
            echo "✅ Package $package is already installed."
        fi
    done
}

# Function to check if required environment variables are set
check_env_vars() {
    echo "🔍 Checking required environment variables..."
    required_vars=("TWINE_USERNAME" "TWINE_PASSWORD")
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            read -p "⚠️  Environment variable $var is not set. Please enter value: " value
            export $var=$value
            echo "✅ Exported $var=$value"
        else
            echo "✅ Environment variable $var is already set."
        fi
    done
}

# Function to create or update .github workflow
create_update_workflow() {
    mkdir -p .github/workflows
    cat > .github/workflows/python-package.yml <<EOL
name: Python package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 .
    - name: Test with pytest
      run: |
        pytest
EOL
    echo "⚙️  GitHub workflow created/updated."
}

# Function to run tests using Pytest
run_tests() {
    pytest
    echo "✅ Tests completed."
}

# Function to lint and format code
lint_format_code() {
    flake8 .
    black .
    echo "✅ Code linted and formatted."
}

# Function to check and update dependencies
check_update_dependencies() {
    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo "⚠️  It seems you haven't activated a virtualenv."
        read -p "Do you want to skip the virtualenv check and install packages anyway? (y/n): " choice
        if [[ "$choice" != "y" ]]; then
            echo "❌ Dependency check canceled. Please activate your virtualenv."
            return
        fi
    fi
    pip-upgrade
    echo "✅ Dependencies checked and updated."
}

# Main loop to display menu and handle user input
initial_checks() {
    check_packages
    check_env_vars
}

main_menu() {
    while true; do
        show_menu
        read -p "Select an option: " choice

        case $choice in
            1)
                clean_dists
                ;;
            2)
                build_dists
                ;;
            3)
                upload_dists
                ;;
            4)
                increment_version patch
                ;;
            5)
                increment_version minor
                ;;
            6)
                increment_version major
                ;;
            7)
                advanced_menu
                ;;
            8)
                echo "Goodbye! 👋"
                exit 0
                ;;
            *)
                echo "❌ Invalid option, please try again."
                ;;
        esac

        echo -e "\nPress any key to continue..."
        read -n 1
    done
}

advanced_menu() {
    while true; do
        show_advanced_menu
        read -p "Select an advanced option: " adv_choice
        case $adv_choice in
            1)
                create_update_workflow
                ;;
            2)
                run_tests
                ;;
            3)
                lint_format_code
                ;;
            4)
                check_update_dependencies
                ;;
            5)
                return
                ;;
            *)
                echo "❌ Invalid option, please try again."
                ;;
        esac
        echo -e "\nPress any key to continue..."
        read -n 1
    done
}

# Run initial checks once
initial_checks

# Start main menu
main_menu
