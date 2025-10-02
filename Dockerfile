# Start from their official image (has all language environments)
FROM multilingualnlp/mdeval:v1

COPY . ./

ENV PYTHONPATH=/workspace
ENV PYTHONUNBUFFERED=1

CMD ["python", "evaluate.py", "--help"]
