#!/bin/bash

# ------------------------------------------
# GyaanPlant APK Decompile Automation Script
# ------------------------------------------

# Set variables
APK_NAME="gyaanplant.apk"
BASE_DIR="$HOME/gyaanplant_automation"
APK_PATH="$BASE_DIR/app/$APK_NAME"
DEST_DIR="reverseenginnering/reverse"
OUTPUT_DIR="$BASE_DIR/$DEST_DIR"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Check if jadx is installed
if ! command -v jadx &> /dev/null
then
    echo "❌ jadx is not installed. Please install it using: brew install jadx"
    exit 1
fi

# Confirm APK file exists
if [ ! -f "$APK_PATH" ]; then
    echo "❌ APK file not found at $APK_PATH"
    exit 1
fi

# Run jadx
echo "🔍 Decompiling $APK_NAME into $DEST_DIR..."
jadx -d "$OUTPUT_DIR" "$APK_PATH"

# Completion message
echo "✅ Decompilation complete. Output stored in: $OUTPUT_DIR"
open "$OUTPUT_DIR"  # Opens folder in Finder (macOS only)

