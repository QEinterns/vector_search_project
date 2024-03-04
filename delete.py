import os

def delete_files(source_dir, target_dir):
    source_files = os.listdir(source_dir)
    target_files = os.listdir(target_dir)

    deleted_files = 0

    for file_name in source_files:
        if file_name in target_files:
            file_path = os.path.join(source_dir, file_name)
            os.remove(file_path)
            deleted_files += 1

    return deleted_files

def main():
    source_directory = '/Users/spatra/Desktop/Movie/Internal_docs/kv_engine'
    target_directory = '/Users/spatra/Desktop/Movie/Internal_docs/dcp'

    deleted_count = delete_files(source_directory, target_directory)
    print(f"Deleted {deleted_count} files from {source_directory} that were also present in {target_directory}.")

if __name__ == "__main__":
    main()
