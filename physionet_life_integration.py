#!/usr/bin/env python3
"""
Quick integration example: PhysioNet → L.I.F.E Platform
Download real EEG data and process with L.I.F.E. algorithm

Run: python physionet_life_integration.py
"""

import asyncio
import json
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


async def quick_demo():
    """Demo: Load PhysioNet data and process with L.I.F.E."""

    print("\n" + "=" * 80)
    print("🧠 L.I.F.E. + PhysioNet Integration Demo")
    print("=" * 80)

    try:
        from physionet_eeg_ingest import PhysioNetIngestor

        print("\n✅ PhysioNet Ingestor loaded")
    except ImportError:
        print("\n❌ Error: physionet_eeg_ingest module not found")
        print("   Make sure physionet_eeg_ingest.py is in the same directory")
        return

    # Initialize ingestor
    ingestor = PhysioNetIngestor()

    # Available datasets
    print("\n📊 Available PhysioNet Datasets:")
    print("  1. bci_iv_2a      - Motor Imagery EEG (22 channels, 250 Hz)")
    print("  2. sleep_edf      - Sleep staging (2 channels, 100 Hz)")
    print("  3. eeg_ecg_coupling - Brain-heart sync (64 channels, 256 Hz)")
    print("  4. pt_seizure     - Seizure data (23 channels, 256 Hz)")
    print("  5. temple_university_seizure - TUH data (21 channels, 250 Hz)")

    # Download example
    dataset_choice = "bci_iv_2a"
    print(f"\n📥 Downloading {dataset_choice}...")
    print("   Subject: 1, Session: 1")

    eeg_data = await ingestor.download_dataset(dataset_choice, subject_id=1, session=1)

    if not eeg_data:
        print("❌ Download failed")
        return

    print(f"✅ Downloaded {len(eeg_data) / (1024 * 1024):.2f} MB")

    # Save and parse
    import tempfile

    temp_dir = tempfile.mkdtemp()
    edf_path = os.path.join(temp_dir, "sample.edf")

    with open(edf_path, "wb") as f:
        f.write(eeg_data)

    print(f"\n📂 Parsing EDF file...")
    eeg_array, metadata = ingestor.parse_edf_file(edf_path)

    if eeg_array is None:
        print("❌ EDF parsing failed (pyedflib may not be installed)")
        print("   Install with: pip install pyedflib")
        return

    print(f"✅ Loaded {eeg_array.shape[0]} channels, {eeg_array.shape[1]} samples")
    print(f"   Duration: {metadata.get('duration_sec', 'N/A')} seconds")
    print(f"   Sampling rate: {metadata.get('sampling_rate', 'N/A')} Hz")

    # Process first channel
    print(f"\n🔬 Processing EEG signal (Channel 1)...")
    results = ingestor.process_eeg_signal(eeg_array[0], sampling_rate=250)

    # Display results
    print("\n📊 Signal Quality Assessment:")
    quality = results["quality"]
    print(f"   Score: {quality['score']:.1f}/100")
    print(f"   Rating: {quality['rating']}")
    print(f"   SNR: {quality['snr_db']:.2f} dB")
    print(f"   Peak-to-Peak: {quality['peak_to_peak_uv']:.2f} µV")
    print(f"   Variance: {quality['variance']:.2f}")

    print("\n📈 Frequency Band Analysis:")
    freq = results["frequency"]
    bands = ["delta", "theta", "alpha", "beta", "gamma"]
    for band in bands:
        key = f"{band}_power_percent"
        if key in freq:
            print(f"   {band.upper():6s}: {freq[key]:6.2f}%")

    print("\n🎯 Artifact Detection:")
    artifacts = results["artifacts"]
    print(f"   Eye Blinks: {artifacts['blink_events']} events")
    print(f"   Blink Percentage: {artifacts['blink_percentage']:.2f}%")
    print(f"   Muscle Artifact Power: {artifacts['muscle_artifact_power']:.4f}")
    print(
        f"   Line Noise (50/60 Hz): {'Detected' if artifacts['line_noise_present'] else 'Clear'}"
    )

    # Summary
    print("\n" + "=" * 80)
    print("✨ Integration Complete!")
    print("=" * 80)
    print("\n📝 Next Steps:")
    print("   1. Process all channels: for i in range(eeg_array.shape[0]): ...")
    print("   2. Export results: converter.numpy_to_csv(eeg_array, 'results.csv')")
    print("   3. Upload to L.I.F.E. platform dashboards")
    print("   4. Run L.I.F.E algorithm: life.process_eeg_stream(eeg_array)")

    # Cleanup
    import shutil

    shutil.rmtree(temp_dir)
    print("\n✅ Temporary files cleaned up")


async def batch_process_subjects():
    """Process multiple subjects from a dataset"""

    from physionet_eeg_ingest import PhysioNetIngestor

    print("\n" + "=" * 80)
    print("🔄 Batch Processing Example: BCI IV-2a (All 9 Subjects)")
    print("=" * 80)

    ingestor = PhysioNetIngestor()
    results = []

    for subject_id in range(1, 10):  # 9 subjects
        print(f"\n📥 Processing Subject {subject_id}...")

        try:
            eeg_data = await ingestor.download_dataset(
                "bci_iv_2a", subject_id=subject_id, session=1
            )

            if eeg_data:
                import shutil
                import tempfile

                temp_dir = tempfile.mkdtemp()
                edf_path = os.path.join(temp_dir, f"S{subject_id:03d}_eeg.edf")

                with open(edf_path, "wb") as f:
                    f.write(eeg_data)

                eeg_array, metadata = ingestor.parse_edf_file(edf_path)

                if eeg_array is not None:
                    processing = ingestor.process_eeg_signal(
                        eeg_array[0], sampling_rate=250
                    )
                    result = {
                        "subject": subject_id,
                        "quality_score": processing["quality"]["score"],
                        "quality_rating": processing["quality"]["rating"],
                        "snr_db": processing["quality"]["snr_db"],
                    }
                    results.append(result)
                    print(f"   ✅ Quality: {result['quality_score']:.1f}/100")

                shutil.rmtree(temp_dir)

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Summary table
    if results:
        print("\n📊 Batch Processing Results:")
        print(
            f"\n{'Subject':<10} {'Quality Score':<15} {'Rating':<10} {'SNR (dB)':<10}"
        )
        print("-" * 45)
        for r in results:
            print(
                f"{r['subject']:<10} {r['quality_score']:<15.1f} "
                f"{r['quality_rating']:<10} {r['snr_db']:<10.2f}"
            )

        avg_quality = sum(r["quality_score"] for r in results) / len(results)
        print(f"\nAverage Quality Score: {avg_quality:.1f}/100 ✨")


def export_example():
    """Example: Export data to different formats"""

    print("\n" + "=" * 80)
    print("💾 Data Export Examples")
    print("=" * 80)

    try:
        import numpy as np

        from physionet_eeg_ingest import DataFormatConverter

        # Create sample data
        sample_data = np.random.randn(22, 1000)  # 22 channels, 1000 samples

        converter = DataFormatConverter()

        # Export to CSV
        print("\n📄 Exporting to CSV...")
        csv_path = "eeg_export.csv"
        channel_names = [
            "Fp1",
            "Fp2",
            "F3",
            "F4",
            "C3",
            "C4",
            "P3",
            "P4",
            "O1",
            "O2",
            "F7",
            "F8",
            "T3",
            "T4",
            "T5",
            "T6",
            "Fz",
            "Cz",
            "Pz",
            "Oz",
            "A1",
            "A2",
        ]
        converter.numpy_to_csv(sample_data, csv_path, channel_names)
        print(f"   ✅ Saved to {csv_path}")

        # Export to NPY
        print("\n📦 Exporting to NPY (NumPy binary)...")
        npy_path = "eeg_export.npy"
        converter.numpy_to_npy(sample_data, npy_path)
        print(f"   ✅ Saved to {npy_path}")

        # Load from CSV
        print("\n📂 Loading from CSV...")
        loaded_data = converter.csv_to_numpy(csv_path, skip_header=1)
        print(f"   ✅ Loaded shape: {loaded_data.shape}")

        print("\n✨ Export/Import cycle complete!")

    except ImportError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🚀 L.I.F.E Platform + PhysioNet Integration Examples")
    print("=" * 80)

    print("\n Choose an option:")
    print("  1. Quick demo (single subject)")
    print("  2. Batch process all 9 subjects")
    print("  3. Data export examples")
    print("  4. Run all examples")

    try:
        choice = input("\nEnter choice (1-4): ").strip()
    except KeyboardInterrupt:
        print("\n\nAborted by user")
        exit(1)

    if choice == "1":
        asyncio.run(quick_demo())
    elif choice == "2":
        asyncio.run(batch_process_subjects())
    elif choice == "3":
        export_example()
    elif choice == "4":
        asyncio.run(quick_demo())
        asyncio.run(batch_process_subjects())
        export_example()
    else:
        print("Invalid choice")
