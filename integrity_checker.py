import os
import hashlib
import argparse
from datetime import datetime

BLOCK_SIZE = 65536

def calculate_hash(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(BLOCK_SIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(BLOCK_SIZE)
        return hasher.hexdigest()
    except IOError:
        return None

def create_baseline(directory, baseline_file):
    print(f"[*] Creating baseline for directory: '{directory}'...")
    baseline_hashes = {}
    
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = calculate_hash(filepath)
            if file_hash:
                relative_path = os.path.relpath(filepath, directory)
                baseline_hashes[relative_path] = file_hash

    try:
        with open(baseline_file, 'w') as f:
            for path, hash_val in baseline_hashes.items():
                f.write(f"{path}:{hash_val}\n")
        print(f"[+] Baseline created successfully: '{baseline_file}'")
        print(f"[+] Monitored {len(baseline_hashes)} files.")
    except IOError:
        print(f"[!] Error: Could not write to baseline file '{baseline_file}'.")

def verify_integrity(directory, baseline_file):
    if not os.path.exists(baseline_file):
        print(f"[!] Error: Baseline file '{baseline_file}' not found.")
        print("[*] Please create a baseline first using the --create flag.")
        return

    print(f"[*] Verifying integrity for directory: '{directory}'...")
    print(f"[*] Using baseline file: '{baseline_file}'")
    
    stored_hashes = {}
    try:
        with open(baseline_file, 'r') as f:
            for line in f:
                path, hash_val = line.strip().split(':', 1)
                stored_hashes[path] = hash_val
    except IOError:
        print(f"[!] Error: Could not read baseline file '{baseline_file}'.")
        return

    current_hashes = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_hash = calculate_hash(filepath)
            if file_hash:
                relative_path = os.path.relpath(filepath, directory)
                current_hashes[relative_path] = file_hash

    modified_files = []
    new_files = []
    ok_files = 0
    
    for path, current_hash in current_hashes.items():
        if path not in stored_hashes:
            new_files.append(path)
        elif stored_hashes[path] != current_hash:
            modified_files.append(path)
        else:
            ok_files += 1

    deleted_files = [path for path in stored_hashes if path not in current_hashes]

    print("\n--- Integrity Check Report ---")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    if not modified_files and not new_files and not deleted_files:
        print(f"✅ SUCCESS: All {ok_files} monitored files are unchanged.")
    else:
        if modified_files:
            print(f"🚨 MODIFIED ({len(modified_files)}):")
            for f in modified_files: print(f"  - {f}")
        if new_files:
            print(f"\n✨ NEW ({len(new_files)}):")
            for f in new_files: print(f"  - {f}")
        if deleted_files:
            print(f"\n🗑️ DELETED ({len(deleted_files)}):")
            for f in deleted_files: print(f"  - {f}")
        
        print(f"\n[*] Summary: {ok_files} files OK, {len(modified_files)} modified, {len(new_files)} new, {len(deleted_files)} deleted.")
    print("----------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Integrity Checker")
    parser.add_argument("directory", help="The directory to monitor.")
    parser.add_argument("--create", action="store_true", help="Create a new baseline for the directory.")
    parser.add_argument("--baseline_file", default="baseline.txt", help="The file to store/read the baseline hashes from (default: baseline.txt).")
    
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"[!] Error: The specified path '{args.directory}' is not a valid directory.")
    elif args.create:
        create_baseline(args.directory, args.baseline_file)
    else:
        verify_integrity(args.directory, args.baseline_file)
        