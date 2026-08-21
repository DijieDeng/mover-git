# File Mover + Git Push

A Python desktop application for moving files into a Git repository and automatically committing and pushing them to a remote repository.

The application provides a Tkinter GUI for scanning files before moving them, identifying files that exceed size limits, splitting transfers into manageable batches, optionally organizing photos and videos by date, and tracking Git push progress.

## Features

* Graphical interface built with Tkinter
* Select a source folder and destination Git repository
* Optionally select a subfolder inside the repository
* Scan and preview files before moving them
* Skip files larger than **100 MB**
* Split files into batches of up to **2 GB**
* Commit and push each batch separately
* Optionally move everything first and create a single commit
* Preserve empty directories when possible
* Display valid files, skipped files, batches, and Git logs
* Track files and data pushed
* Automatically detect the repository's GitHub URL
* Optional photo and video organization

## Media Organization

The application can optionally organize supported media files using their date information.

Supported media types:

```text
.jpg
.jpeg
.png
.heic
.mp4
.mov
.avi
.aae
```

When media organization is enabled, the application can:

* Place files into `YYYY-MM-DD` folders
* Rename files using timestamps
* Use image EXIF metadata when available
* Fall back to the file modification time when necessary
* Automatically avoid filename collisions

Example:

```text
Source
└── IMG_1234.JPG

Destination
└── 2026-08-21
    └── 2026-08-21 14_32_10.JPG
```

## Requirements

* Python 3
* Git
* Tkinter
* Pillow
* pillow-heif

OpenCV is optional and is used for supported video handling when installed.

Install the Python dependencies with:

```bash
pip install Pillow pillow-heif opencv-python
```

If you do not need the optional OpenCV functionality, you can install only:

```bash
pip install Pillow pillow-heif
```

Git must also be installed and available from the command line:

```bash
git --version
```

## Repository Setup

The destination folder must already be a Git repository.

For example:

```bash
git clone <repository-url>
cd <repository-name>
```

Alternatively, initialize a repository manually:

```bash
mkdir my-repository
cd my-repository
git init
git remote add origin <repository-url>
```

Make sure authentication with the remote Git provider is configured before using the application.

## Usage

Run the application:

```bash
python main.py
```

Replace `main.py` with the actual filename of the program if it has a different name.

### 1. Select the Source Folder

Click **Browse** next to **Source folder** and select the directory containing the files you want to move.

### 2. Select the Destination Repository

Click **Browse** next to **Destination repo folder** and select an existing local Git repository.

The selected directory must contain a `.git` directory.

### 3. Choose a Destination Subfolder

Optionally select a folder inside the Git repository.

If no subfolder is selected, files are moved into the repository root.

### 4. Configure Git Options

You can configure:

**Commit prefix**

Adds custom text to automatically generated commit messages.

**Branch**

The branch pushed to the `origin` remote. The default is:

```text
main
```

**Commit/push after each 2 GB batch**

When enabled, every batch is committed and pushed before processing the next batch.

**Recreate empty directories when possible**

Attempts to preserve empty directories from the source structure.

### 5. Configure Media Organization

Enable **Organize media by date taken / modified** to activate media organization.

Additional options allow you to:

* Create `YYYY-MM-DD` folders
* Rename media using timestamps
* Restrict organization to supported media formats

### 6. Scan and Preview

Click:

```text
1) Scan and Preview
```

The application scans the source directory and displays:

* Valid files
* Skipped files
* Destination paths
* Batch assignments
* Total file sizes
* Number of required Git batches

No files are moved during the scan.

### 7. Move and Push

After reviewing the preview, click:

```text
2) Move + Git Push
```

The application asks for confirmation before modifying files.

It then:

1. Creates applicable destination directories.
2. Moves files into the repository.
3. Runs `git add .`.
4. Creates a commit.
5. Pushes the commit to the configured branch.
6. Repeats the process for additional batches when necessary.

Progress is displayed in the application while processing.

## File Size Limits

The application uses the following limits:

| Limit                   |   Size |
| ----------------------- | -----: |
| Maximum individual file | 100 MB |
| Maximum batch           |   2 GB |

Files larger than 100 MB are skipped and displayed in the **Skipped files** tab.

> This application does not automatically configure Git LFS for files exceeding normal Git hosting limits.

## Commit Messages

Commit messages are generated automatically.

Example:

```text
[08][21][2026] [14:32:10] update - 125 files - 842.31 MB
```

When multiple batches are required, later commits receive a batch number.

For example:

```text
[08][21][2026] [14:32:10] update - 125 files - 842.31 MB
[08][21][2026] [14:40:22] update 2 - 98 files - 1.72 GB
```

A custom commit prefix can replace `update`.

## Git Commands

The application automatically performs the equivalent of:

```bash
git status --short
git add .
git status --short
git commit -m "<generated commit message>"
git push -u origin <branch>
```

If no Git changes are detected after staging, the commit and push are skipped.

## Safety Checks

Before moving files, the application verifies that:

* The source directory exists
* The destination directory exists
* The destination is a Git repository
* The selected subfolder remains inside the repository
* The source is not inside the destination
* The destination is not inside the source

Symlinks are skipped during scanning.

The application also provides a preview before files are moved and asks for confirmation before starting the move and Git operations.

## Important

This application **moves** files rather than copying them.

After a successful move, the original files will no longer remain in their original locations.

Back up important files before using the application.

Git operations can also modify and push other uncommitted changes already present in the selected repository because the application uses:

```bash
git add .
```

For that reason, it is recommended to start with a clean Git working tree.

## Project Structure

A minimal project could look like:

```text
file-mover-git/
├── main.py
├── README.md
└── requirements.txt
```

Example `requirements.txt`:

```text
Pillow
pillow-heif
opencv-python
```

If OpenCV is not needed:

```text
Pillow
pillow-heif
```

## Troubleshooting

### "Not a Git repo"

The destination directory does not contain a `.git` folder.

Clone or initialize the repository before selecting it.

### Git push fails

Verify:

* Git is installed
* The repository has an `origin` remote
* The configured branch exists or can be created
* Your Git credentials or SSH keys are configured
* You have permission to push to the remote repository

Check the application's **Log** tab for the Git error message.

### Files are skipped

Files larger than 100 MB are intentionally skipped. Symlinks and unreadable files are also skipped.

Check the **Skipped files** tab for the reason.

### Media has the wrong date

For supported images, the application attempts to read EXIF date metadata. If usable metadata cannot be found, it falls back to the file's modification time.

Video files also fall back to their filesystem modification time.

## Disclaimer

File and Git operations can result in data loss if used incorrectly.

Review the scan preview, maintain backups of important files, and verify the destination repository before starting a move.
