#!/usr/bin/env python3
"""
🧠 Interactive EEG Data Ingestion Tool
PhysioNet & Open Science Real-Time Search & Download

Features:
- Search for EEG datasets by type
- Real-time dataset discovery
- Direct download from PhysioNet/OpenNeuro
- Automatic processing & analysis
- Azure Blob Storage upload capability

Copyright 2025 - Sergio Paya Borrull
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

import requests

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class EEGDatasetSearcher:
    """Search for EEG datasets by type and criteria"""

    # Comprehensive dataset catalog
    DATASET_CATALOG = {
        # PhysioNet Motor Imagery
        "motor_imagery": {
            "name": "Motor Imagery",
            "sources": [
                {
                    "id": "bci_iv_2a",
                    "name": "BCI Competition IV-2a",
                    "source": "PhysioNet",
                    "url": "https://physionet.org/files/eegmmidb/1.0.0",
                    "subjects": 9,
                    "channels": 22,
                    "sampling_rate": 250,
                    "description": "Motor imagery EEG during movement imagination",
                    "paper": "https://doi.org/10.1109/TNSRE.2008.927637",
                }
            ],
        },
        # PhysioNet Sleep
        "sleep": {
            "name": "Sleep Staging",
            "sources": [
                {
                    "id": "sleep_edf",
                    "name": "Sleep-EDF",
                    "source": "PhysioNet",
                    "url": "https://physionet.org/files/sleep-edfx/1.0.0",
                    "subjects": 197,
                    "channels": 2,
                    "sampling_rate": 100,
                    "description": "Full-night sleep recordings with stage annotations",
                    "paper": "https://doi.org/10.1038/sdata.2018.3",
                }
            ],
        },
        # Brain-Heart Coupling
        "brain_heart": {
            "name": "EEG-ECG Coupling",
            "sources": [
                {
                    "id": "eeg_ecg_coupling",
                    "name": "EEG-ECG Coupling",
                    "source": "PhysioNet",
                    "url": "https://physionet.org/files/eegmmidb/1.0.0",
                    "subjects": 109,
                    "channels": 64,
                    "sampling_rate": 256,
                    "description": "Brain-heart synchronization during rest",
                    "paper": "https://doi.org/10.1038/srep00508",
                }
            ],
        },
        # Seizure Detection
        "seizure": {
            "name": "Seizure Detection",
            "sources": [
                {
                    "id": "chb_mit",
                    "name": "CHB-MIT Scalp EEG Database",
                    "source": "PhysioNet",
                    "url": "https://physionet.org/files/chbmit/1.0.0",
                    "subjects": 24,
                    "channels": 23,
                    "sampling_rate": 256,
                    "description": "Pediatric seizure database",
                    "paper": "https://doi.org/10.1109/IEMBS.2005.1617480",
                },
                {
                    "id": "temple_seizure",
                    "name": "Temple University Seizure Database",
                    "source": "PhysioNet",
                    "url": "https://physionet.org/files/tuh_eeg/1.0.0",
                    "subjects": 109,
                    "channels": 21,
                    "sampling_rate": 250,
                    "description": "Temple Hospital EEG recordings",
                    "paper": "https://doi.org/10.1038/sdata.2016.47",
                },
            ],
        },
        # Clinical Abnormalities
        "abnormality": {
            "name": "Clinical Abnormality Detection",
            "sources": [
                {
                    "id": "tuh_abnormal",
                    "name": "TUH Abnormal EEG",
                    "source": "PhysioNet",
                    "url": "https://physionet.org/files/tuh_eeg_abnormal/1.0.0",
                    "subjects": 200,
                    "channels": 21,
                    "sampling_rate": 250,
                    "description": "Abnormal vs normal EEG classification",
                    "paper": "https://doi.org/10.1038/sdata.2016.47",
                }
            ],
        },
        # Neuroplasticity
        "neuroplasticity": {
            "name": "Neuroplasticity & Learning",
            "sources": [
                {
                    "id": "bci_iv_2a",
                    "name": "BCI Motor Learning",
                    "source": "PhysioNet",
                    "url": "https://physionet.org/files/eegmmidb/1.0.0",
                    "subjects": 9,
                    "channels": 22,
                    "sampling_rate": 250,
                    "description": "Motor imagery learning progression",
                    "paper": "https://doi.org/10.1109/TNSRE.2008.927637",
                }
            ],
        },
        # Resting State
        "resting_state": {
            "name": "Resting State EEG",
            "sources": [
                {
                    "id": "openneuro_resting",
                    "name": "OpenNeuro Resting State",
                    "source": "OpenNeuro",
                    "url": "https://openneuro.org",
                    "subjects": 300,
                    "channels": 64,
                    "sampling_rate": 256,
                    "description": "BIDS-compliant resting state data",
                    "paper": "https://openneuro.org/",
                }
            ],
        },
        # Cognitive Tasks
        "cognitive": {
            "name": "Cognitive Task EEG",
            "sources": [
                {
                    "id": "openneuro_cognitive",
                    "name": "OpenNeuro Cognitive Tasks",
                    "source": "OpenNeuro",
                    "url": "https://openneuro.org",
                    "subjects": 200,
                    "channels": 32,
                    "sampling_rate": 512,
                    "description": "Working memory, attention, N-back tasks",
                    "paper": "https://openneuro.org/",
                }
            ],
        },
        # Pathological
        "pathological": {
            "name": "Pathological EEG",
            "sources": [
                {
                    "id": "chb_mit",
                    "name": "Seizure Pathology",
                    "source": "PhysioNet",
                    "url": "https://physionet.org/files/chbmit/1.0.0",
                    "subjects": 24,
                    "channels": 23,
                    "sampling_rate": 256,
                    "description": "Seizure & epilepsy diagnosis",
                    "paper": "https://doi.org/10.1109/IEMBS.2005.1617480",
                }
            ],
        },
    }

    def __init__(self):
        self.selected_dataset = None
        self.search_results = []

    def display_menu(self):
        """Display main menu"""
        print("\n" + "=" * 80)
        print("🧠 L.I.F.E. Interactive EEG Data Ingestion Tool")
        print("=" * 80)
        print("\n📊 Select EEG Dataset Type:\n")

        categories = list(self.DATASET_CATALOG.keys())
        for i, category in enumerate(categories, 1):
            info = self.DATASET_CATALOG[category]
            print(f"  {i}. {info['name']}")

        print(f"  {len(categories) + 1}. Search by keyword")
        print(f"  {len(categories) + 2}. List all datasets")
        print(f"  {len(categories) + 3}. Exit")

        return categories

    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """Search datasets by keyword"""
        keyword_lower = keyword.lower()
        results = []

        for category, category_data in self.DATASET_CATALOG.items():
            for source in category_data["sources"]:
                if (
                    keyword_lower in source["name"].lower()
                    or keyword_lower in source["description"].lower()
                    or keyword_lower in category.lower()
                ):
                    results.append(source)

        return results

    def display_dataset_details(self, dataset: Dict):
        """Display detailed information about a dataset"""
        print("\n" + "=" * 80)
        print(f"📊 Dataset: {dataset['name']}")
        print("=" * 80)
        print(f"Source:          {dataset['source']}")
        print(f"Subjects:        {dataset['subjects']}")
        print(f"Channels:        {dataset['channels']}")
        print(f"Sampling Rate:   {dataset['sampling_rate']} Hz")
        print(f"Description:     {dataset['description']}")
        print(f"Paper:           {dataset['paper']}")
        print(f"URL:             {dataset['url']}")
        print("=" * 80)

    def display_all_datasets(self):
        """List all available datasets"""
        print("\n" + "=" * 80)
        print("📊 All Available EEG Datasets")
        print("=" * 80)

        idx = 1
        for category, category_data in self.DATASET_CATALOG.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for source in category_data["sources"]:
                print(f"  {idx}. {source['name']}")
                print(f"     Source: {source['source']}")
                print(f"     Subjects: {source['subjects']}")
                print(f"     Sampling: {source['sampling_rate']} Hz")
                idx += 1


class RealTimeDownloader:
    """Download datasets in real-time from PhysioNet/OpenNeuro"""

    def __init__(self):
        self.cache_dir = "physionet_cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    async def download_dataset(
        self, dataset_id: str, subject_id: int = 1, session: int = 1
    ) -> Optional[bytes]:
        """Download dataset in real-time"""

        print(f"\n📥 Downloading {dataset_id}...")
        print(f"   Subject: {subject_id}")
        print(f"   Session: {session}")

        try:
            if dataset_id == "bci_iv_2a":
                return await self._download_bci_iv_2a(subject_id, session)
            elif dataset_id == "sleep_edf":
                return await self._download_sleep_edf(subject_id)
            elif dataset_id == "chb_mit":
                return await self._download_chb_mit(subject_id)
            elif dataset_id == "tuh_abnormal":
                return await self._download_tuh_abnormal(subject_id)
            else:
                print(f"❌ Dataset {dataset_id} download not yet configured")
                return None

        except Exception as e:
            logger.error(f"Download error: {e}")
            print(f"❌ Download failed: {e}")
            return None

    async def _download_bci_iv_2a(self, subject: int, session: int) -> Optional[bytes]:
        """Download BCI IV-2a with progress"""
        url = (
            f"https://physionet.org/files/eegmmidb/1.0.0/S{subject:03d}/"
            f"S{subject:03d}R{session:02d}.edf"
        )

        try:
            print(f"📡 Connecting to PhysioNet...")
            response = requests.get(url, timeout=60, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            downloaded = 0

            print(f"📊 File size: {total_size / (1024 * 1024):.2f} MB")
            print(f"⏳ Downloading...")

            content = b""
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    content += chunk
                    downloaded += len(chunk)
                    if total_size:
                        progress = (downloaded / total_size) * 100
                        print(
                            f"   Progress: {progress:.1f}% "
                            f"({downloaded / (1024 * 1024):.2f}/{total_size / (1024 * 1024):.2f} MB)",
                            end="\r",
                        )

            print(
                f"\n✅ Downloaded {len(content) / (1024 * 1024):.2f} MB "
                f"({len(content)} bytes)"
            )
            return content

        except requests.RequestException as e:
            logger.error(f"BCI IV-2a download failed: {e}")
            print(f"❌ Failed: {e}")
            return None

    async def _download_sleep_edf(self, subject: int) -> Optional[bytes]:
        """Download Sleep-EDF"""
        url = (
            f"https://physionet.org/files/sleep-edfx/1.0.0/sleep-cassette/"
            f"SC4{subject:03d}E0-PSG.edf"
        )

        try:
            print(f"📡 Connecting to PhysioNet...")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            print(f"✅ Downloaded {len(response.content) / (1024 * 1024):.2f} MB")
            return response.content
        except requests.RequestException as e:
            print(f"❌ Failed: {e}")
            return None

    async def _download_chb_mit(self, subject: int) -> Optional[bytes]:
        """Download CHB-MIT seizure data"""
        url = f"https://physionet.org/files/chbmit/1.0.0/chb{subject:02d}/chb{subject:02d}_01.edf"

        try:
            print(f"📡 Connecting to PhysioNet...")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            print(f"✅ Downloaded {len(response.content) / (1024 * 1024):.2f} MB")
            return response.content
        except requests.RequestException as e:
            print(f"❌ Failed: {e}")
            return None

    async def _download_tuh_abnormal(self, subject: int) -> Optional[bytes]:
        """Download TUH abnormal data"""
        url = (
            f"https://physionet.org/files/tuh_eeg_abnormal/1.0.0/"
            f"dev/abnormal/01_tcp_le/000/{subject:06d}.edf"
        )

        try:
            print(f"📡 Connecting to PhysioNet...")
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            print(f"✅ Downloaded {len(response.content) / (1024 * 1024):.2f} MB")
            return response.content
        except requests.RequestException as e:
            print(f"❌ Failed: {e}")
            return None


class AzureUploader:
    """Upload processed data to Azure Blob Storage"""

    def __init__(self):
        self.container_name = "eeg-data"

    async def upload_to_azure(self, file_path: str, dataset_info: Dict) -> bool:
        """Upload EEG data to Azure Blob Storage"""

        try:
            from azure.identity import DefaultAzureCredential
            from azure.storage.blob import BlobClient

            print(f"\n📤 Preparing Azure upload...")
            print(f"   Container: {self.container_name}")
            print(f"   Dataset: {dataset_info['name']}")

            credential = DefaultAzureCredential()

            # Get storage account from environment or config
            storage_account = os.getenv("AZURE_STORAGE_ACCOUNT", "stlifeplatformprod")
            blob_name = f"{dataset_info['source']}/{dataset_info['name']}/S{dataset_info.get('subject_id', 1):03d}.edf"

            blob_url = (
                f"https://{storage_account}.blob.core.windows.net/"
                f"{self.container_name}/{blob_name}"
            )

            print(f"📡 Uploading to Azure...")
            print(f"   URL: {blob_url}")

            with open(file_path, "rb") as data:
                blob_client = BlobClient(blob_url, credential=credential)
                blob_client.upload_blob(data, overwrite=True)

            print(f"✅ Successfully uploaded to Azure!")
            return True

        except ImportError:
            print("⚠️  Azure SDK not installed. Install with:")
            print("   pip install azure-storage-blob azure-identity")
            return False
        except Exception as e:
            logger.error(f"Azure upload failed: {e}")
            print(f"❌ Upload failed: {e}")
            return False


class InteractiveIngestor:
    """Main interactive ingestion tool"""

    def __init__(self):
        self.searcher = EEGDatasetSearcher()
        self.downloader = RealTimeDownloader()
        self.uploader = AzureUploader()

    async def run(self):
        """Main interactive loop"""

        while True:
            categories = self.searcher.display_menu()

            try:
                choice = input("\n👉 Enter your choice: ").strip()

                if not choice.isdigit():
                    print("❌ Invalid input. Please enter a number.")
                    continue

                choice_num = int(choice)

                # Exit
                if choice_num == len(categories) + 3:
                    print("\n👋 Goodbye!")
                    break

                # List all
                elif choice_num == len(categories) + 2:
                    self.searcher.display_all_datasets()
                    continue

                # Search by keyword
                elif choice_num == len(categories) + 1:
                    keyword = input("\n🔍 Enter search keyword: ").strip()
                    results = self.searcher.search_by_keyword(keyword)

                    if results:
                        print(f"\n✅ Found {len(results)} dataset(s):")
                        for i, result in enumerate(results, 1):
                            print(f"  {i}. {result['name']} ({result['source']})")

                        idx = input(
                            "\n👉 Select dataset (or press Enter to skip): "
                        ).strip()
                        if idx.isdigit() and 1 <= int(idx) <= len(results):
                            dataset = results[int(idx) - 1]
                            await self._download_and_process(dataset)
                    else:
                        print(f"❌ No datasets found for '{keyword}'")

                # Category selection
                elif 1 <= choice_num <= len(categories):
                    category = categories[choice_num - 1]
                    category_data = self.searcher.DATASET_CATALOG[category]

                    print(f"\n📊 {category_data['name']} - Available Sources:")
                    for i, source in enumerate(category_data["sources"], 1):
                        print(
                            f"  {i}. {source['name']} ({source['subjects']} subjects, "
                            f"{source['channels']} channels, {source['sampling_rate']} Hz)"
                        )

                    src_choice = input("\n👉 Select source: ").strip()
                    if src_choice.isdigit() and 1 <= int(src_choice) <= len(
                        category_data["sources"]
                    ):
                        dataset = category_data["sources"][int(src_choice) - 1]
                        await self._download_and_process(dataset)

                else:
                    print("❌ Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user.")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"❌ Error: {e}")

    async def _download_and_process(self, dataset: Dict):
        """Download and process selected dataset"""

        self.searcher.display_dataset_details(dataset)

        # Get subject and session
        try:
            subject_id = int(
                input(f"\n👉 Enter subject ID (1-{dataset['subjects']}): ").strip()
            )
            session_id = 1

            if dataset["id"] in ["bci_iv_2a"]:
                session_id = int(input("👉 Enter session ID (1-2): ").strip())

        except ValueError:
            print("❌ Invalid input")
            return

        # Download
        print(f"\n⏳ Starting download...")
        eeg_data = await self.downloader.download_dataset(
            dataset["id"], subject_id=subject_id, session=session_id
        )

        if not eeg_data:
            return

        # Save locally
        local_file = os.path.join(
            self.downloader.cache_dir,
            f"{dataset['id']}_S{subject_id:03d}_session{session_id}.edf",
        )

        with open(local_file, "wb") as f:
            f.write(eeg_data)

        print(f"✅ Saved locally: {local_file}")

        # Upload to Azure
        upload_choice = (
            input("\n❓ Upload to Azure Blob Storage? (y/n): ").strip().lower()
        )
        if upload_choice == "y":
            dataset_info = {
                "name": dataset["name"],
                "source": dataset["source"],
                "subject_id": subject_id,
                "session": session_id,
            }
            await self.uploader.upload_to_azure(local_file, dataset_info)

        # Process with L.I.F.E.
        process_choice = (
            input("\n❓ Process with L.I.F.E. algorithm? (y/n): ").strip().lower()
        )
        if process_choice == "y":
            await self._process_with_life(local_file, dataset)

    async def _process_with_life(self, file_path: str, dataset: Dict):
        """Process downloaded EEG with L.I.F.E. algorithm"""

        print(f"\n🧠 Processing with L.I.F.E. algorithm...")

        try:
            from physionet_eeg_ingest import PhysioNetIngestor

            ingestor = PhysioNetIngestor()
            eeg_array, metadata = ingestor.parse_edf_file(file_path)

            if eeg_array is not None:
                results = ingestor.process_eeg_signal(eeg_array[0])

                print(f"\n✅ Processing Complete!")
                print(f"\n📊 Quality Assessment:")
                quality = results["quality"]
                print(f"   Score: {quality['score']:.1f}/100")
                print(f"   Rating: {quality['rating']}")
                print(f"   SNR: {quality['snr_db']:.2f} dB")

                print(f"\n📈 Frequency Analysis:")
                for band in ["delta", "theta", "alpha", "beta", "gamma"]:
                    key = f"{band}_power_percent"
                    if key in results["frequency"]:
                        print(f"   {band.upper()}: {results['frequency'][key]:.2f}%")

        except ImportError:
            print("⚠️  physionet_eeg_ingest module not available")
        except Exception as e:
            print(f"❌ Processing error: {e}")


async def main():
    """Main entry point"""

    print("\n" + "=" * 80)
    print("🚀 L.I.F.E. Interactive EEG Data Ingestion Tool")
    print("=" * 80)
    print("\nThis tool enables you to:")
    print("  ✓ Search for EEG datasets by type")
    print("  ✓ Download in real-time from PhysioNet/OpenScience")
    print("  ✓ Upload to Azure Blob Storage")
    print("  ✓ Process with L.I.F.E. algorithm")
    print("=" * 80)

    ingestor = InteractiveIngestor()
    await ingestor.run()


if __name__ == "__main__":
    asyncio.run(main())
