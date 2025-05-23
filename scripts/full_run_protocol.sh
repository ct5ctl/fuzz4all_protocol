#!/bin/bash

# List of protocols to fuzz
protocols=("bftpd" "dcmtk" "forked-daapd" "google_quiche" "lightftp" "live555" "proftpd" "pureftpd")

# Set default parameters (can override via environment variables)
BATCH_SIZE="${FUZZING_BATCH_SIZE:-30}"
MODEL_NAME="${FUZZING_MODEL:-bigcode/starcoderbase}"
DEVICE="${FUZZING_DEVICE:-cuda}"

echo "Starting Fuzz4All for protocol servers..."
echo "BATCH_SIZE: $BATCH_SIZE"
echo "MODEL_NAME: $MODEL_NAME"
echo "DEVICE: $DEVICE"
echo ""

for target in "${protocols[@]}"; do
    config="/home/Fuzz4All/config/full_run/${target}.yaml"
    folder="outputs/full_run/${target}/"
    target_name="placeholder-for-${target}"  # Just a placeholder. Real execution logic is in the Target class.

    echo "=============================="
    echo "Fuzzing Target: $target"
    echo "Using Config: $config"
    echo "=============================="

    if [ "$DEVICE" = "gpu" ] || [ "$DEVICE" = "cuda" ]; then
        python Fuzz4All/fuzz.py --config "$config" main_with_config \
                                --folder "$folder" \
                                --batch_size "$BATCH_SIZE" \
                                --model_name "$MODEL_NAME" \
                                --target "$target_name"
    else
        python Fuzz4All/fuzz.py --config "$config" main_with_config \
                                --folder "$folder" \
                                --batch_size "$BATCH_SIZE" \
                                --model_name "$MODEL_NAME" \
                                --cpu \
                                --target "$target_name"
    fi

    echo ""
done
