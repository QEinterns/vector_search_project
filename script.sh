
CURRENT_DIR=$(pwd)

brew update
brew install openssl@1.1 python3

echo 'export PATH="/usr/local/bin:"$PATH' >> ~/.zshrc
source ~/.zshrc

python3 -m venv myenv3

# Activate the virtual environment
source myenv3/bin/activate

# Upgrade pip
pip install --upgrade pip

sudo -H python3 -m pip install couchbase

pip install -r "${CURRENT_DIR}/requirements.txt"

# Create the modelfile
MODELFILE="${CURRENT_DIR}/modelfile"
touch "${MODELFILE}"

MODELFILE1="${CURRENT_DIR}/modelfile1"
touch "${MODELFILE1}"


echo "FROM \"${CURRENT_DIR}/architect_chat_models/architect_model.gguf\"" > "${MODELFILE}"
echo "PARAMETER stop \"<|im_start|>\"" >> "${MODELFILE}"
echo "PARAMETER stop \"<|im_end|>\"" >> "${MODELFILE}"
echo "TEMPLATE """ >> "${MODELFILE}"
echo "<|im_start|>system" >> "${MODELFILE}"
echo "{{ .System }}<|im_end|>" >> "${MODELFILE}"
echo "<|im_start|>user" >> "${MODELFILE}"
echo "{{ .Prompt }}<|im_end|>" >> "${MODELFILE}"
echo "<|im_start|>assistant" >> "${MODELFILE}"
echo '"""' >> "${MODELFILE}"

# Run Ollama command for architect1
ollama create architect1 -f "${MODELFILE}"

# Update the modelfile content for couch1
echo "FROM \"${CURRENT_DIR}/doc_chat_models/ggml-model-q8_0.gguf\"" > "${MODELFILE1}"
echo "PARAMETER stop \"<|im_start|>\"" >> "${MODELFILE1}"
echo "PARAMETER stop \"<|im_end|>\"" >> "${MODELFILE1}"
echo "TEMPLATE """ >> "${MODELFILE1}"
echo "<|im_start|>system" >> "${MODELFILE1}"
echo "{{ .System }}<|im_end|>" >> "${MODELFILE1}"
echo "<|im_start|>user" >> "${MODELFILE1}"
echo "{{ .Prompt }}<|im_end|>" >> "${MODELFILE1}"
echo "<|im_start|>assistant" >> "${MODELFILE1}"
echo '"""' >> "${MODELFILE1}"

# Run Ollama command for couch1
ollama create couch1 -f "${MODELFILE}"

# Run Flask application
python app.py
