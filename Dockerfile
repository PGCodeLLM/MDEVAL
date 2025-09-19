# 1. Start from their official image (has all language environments)
FROM multilingualnlp/mdeval:v1

# 2. Copy ALL necessary files (since official image only has env, no code)
COPY . ./

# 3. Install packages
RUN pip install --no-cache-dir -r requirements.txt

# 4. Set environment variables
ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

# Ready to run evaluation
CMD ["python", "evaluate.py", "--help"]
