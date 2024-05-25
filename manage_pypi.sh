#!/bin/bash

# Function to display the menu
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
    echo "7. Exit"
}

# Function to clean old distributions
clean_dists() {
    rm -rf dist/*
    echo "Old distributions cleaned."
}

# Function to build new distributions
build_dists() {
    python setup.py sdist bdist_wheel
    echo "New distributions built."
}

# Function to upload distributions to PyPI
upload_dists() {
    twine upload dist/*
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
    echo "Version incremented to $new_version."
}

# Main loop to display menu and handle user input
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
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid option, please try again."
            ;;
    esac

    echo -e "\nPress any key to continue..."
    read -n 1
done
