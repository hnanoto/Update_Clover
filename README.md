# 🍀 Update_Clover Bootloader Updater

**Update_Clover** is an open-source, automated Python script designed to safely, effortlessly, and intelligently update your Hackintosh's **Clover Bootloader** environment to the latest available releases.

Built with a focus on safety and UI clarity, this tool goes beyond merely replacing EFI files. It handles complex XML patching to keep your `.plist` modern, prevents boot issues through preemptive backups, and smoothly translates the experience natively for global users.

---

## ✨ Features

- **🌐 Smart Source Routing (API):** Prioritizes direct downloads from the official [CloverHackyColor](https://github.com/CloverHackyColor/CloverBootloader) GitHub repository, featuring an auto-fallback to verified forks if standard servers are offline or rate-limited.
- **🔍 Advanced EFI & FAT32 Detection**: Scans through all your macOS physical/synthesized disks—including USB installers and standard FAT32 thumb drives—providing rich UI details (name, identifier, space, and format flag).
- **🛡️ Surgical `config.plist` Validator:** The heart of the script parses memory-safe XML dictionaries (`plistlib`). It smoothly merges modern Clover `Quirks`/`KernelAndKextPatches` structures (such as `KextsToBlock` or OpenCore-like `BooterQuirks`) into your active `config.plist` directly from the freshly downloaded `Sample.plist`, strictly avoiding the erasure of any custom user DSDTs, properties, or patches!
- **📦 Intelligent UEFI Drivers Upgrade:** Instead of wiping custom driver sets, the script carefully copies over only modern `.efi` replacements while introducing specific requirements like `HFSPlus.efi` from OcBinaryData. 
- **💾 Automatic Fallback Backups:** Creates real-time, time-stamped `EFI-Backup-*` copies of your entire boot cycle directly on your home partition prior to any file operations, alongside a `.bak` safety iteration of your `config.plist` during validation.
- **🗣️ Dynamic Multi-Language Layout:** Interfaces effortlessly adapt to your active macOS `AppleLocale` (Fully translated for English and Portuguese users).

---

## 🚀 Getting Started

### Prerequisites
- Operating System: **macOS** (Catalina or newer recommended).
- Runtime: **Python 3.x** installed in your ecosystem.

### Installation & Execution

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/hnanoto/Update_Clover.git
   cd Update_Clover/update_clover
   ```

2. Make sure the bundled `.command` file has execution permissions:
   ```bash
   chmod +x RunClover_Updater.command
   ```

3. Launch the Terminal GUI:
   - Double-click the `RunClover_Updater.command` file from Finder.
   - Or execute it manually:
     ```bash
     ./RunClover_Updater.command
     ```

---

## ⚙️ How It Works (The Menu)

Upon granting access, the program unpacks Clover locally and surfaces a visually intuitive menu containing four major actions:

1. **Update BOOTX64.efi and CLOVERX64.efi**: Quickly syncs core boot bridges.
2. **Update Drivers**: Analyzes your current `.efi` UEFI folder components and patches updates securely side-by-side. 
3. **Full Update**: Automatically triggers Options 1 and 2 sequentially for standard maintenance.
4. **Validate config.plist (Add Quirks/Keys)**: Triggers the non-destructive XML parser to push new mandatory boot properties into your specific Clover setup without risking breaking existing hardware patches.

---

## 🤝 Contribution

Contributions, issues, and feature requests are welcome! 
Feel free to open a Pull Request if you spot a bug or want to introduce experimental fallback mechanics.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
