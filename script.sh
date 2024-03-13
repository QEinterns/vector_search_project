
CURRENT_DIR=$(pwd)

brew update
brew install openssl@1.1 python3

echo 'export PATH="/usr/local/bin:"$PATH' >> ~/.zshrc
source ~/.zshrc

# python3 -m venv cbaap

# Activate the virtual environment
source cbaap/bin/activate

# Upgrade pip
pip install --upgrade pip

sudo -H python3 -m pip install couchbase

pip install -r "${CURRENT_DIR}/requirements.txt"

# Create the modelfile
MODELFILE="${CURRENT_DIR}/modelfile"
touch "${MODELFILE}"

echo "FROM \"${CURRENT_DIR}/architect_model.gguf\"" > "${MODELFILE}"
echo "PARAMETER stop \"<|im_start|>\"" >> "${MODELFILE}"
echo "PARAMETER stop \"<|im_end|>\"" >> "${MODELFILE}"
echo "TEMPLATE \"\"\"" >> "${MODELFILE}"
echo "<|im_start|>system" >> "${MODELFILE}"
echo "{{ .System }}<|im_end|>" >> "${MODELFILE}"
echo "<|im_start|>user" >> "${MODELFILE}"
echo "{{ .Prompt }}<|im_end|>" >> "${MODELFILE}"
echo "<|im_start|>assistant" >> "${MODELFILE}"
echo '"""' >> "${MODELFILE}"

# Run Ollama command for architect1
ollama create architect2 -f "${MODELFILE}"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define the file path
FILE_TO_DELETE="${SCRIPT_DIR}/modelfile"

# Delete the file
rm -f "${FILE_TO_DELETE}"

MODELFILE="${CURRENT_DIR}/modelfile"
touch "${MODELFILE}"

# Update the modelfile content for couch1
echo "FROM \"${CURRENT_DIR}/doc_chat_model.gguf\"" > "${MODELFILE}"
echo "PARAMETER stop \"<|im_start|>\"" >> "${MODELFILE}"
echo "PARAMETER stop \"<|im_end|>\"" >> "${MODELFILE}"
echo "TEMPLATE \"\"\"" >> "${MODELFILE}"
echo "<|im_start|>system" >> "${MODELFILE}"
echo "{{ .System }}<|im_end|>" >> "${MODELFILE}"
echo "<|im_start|>user" >> "${MODELFILE}"
echo "{{ .Prompt }}<|im_end|>" >> "${MODELFILE}"
echo "<|im_start|>assistant" >> "${MODELFILE}"
echo '"""' >> "${MODELFILE}"

# Run Ollama command for couch1
ollama create couch2 -f "${MODELFILE}"

# Run Flask application
python app.py
