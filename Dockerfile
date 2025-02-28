# Stage 1: Build Stage
FROM python:3.10-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker's layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Preload the DialoGPT model
RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small', padding_side='left'); \
    model = AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-small')"

# Stage 2: Runtime Stage
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8080

# Start the app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
