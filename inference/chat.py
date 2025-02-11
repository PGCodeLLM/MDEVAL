from openai import OpenAI
import sys
import json
import os

client = OpenAI(api_key="")

def chat(query,model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": query},
        ],
        temperature=0,
        max_tokens=4096,
        stream=False
    )
    print(response.choices[0].message.content)
    
    return response.choices[0].message.content

if __name__ == '__main__':
    language_list = [
                'C',
                'C#',
                'Clisp',
                'CPP',
                'F#',
                'Go',
                'HTML',
                'JavaScript',
                'Java',
                'JSON',
                'Julia',
                'Markdown',
                'PHP',
                'Pascal',
                'Python',
                'R',
                'Ruby',
                'Rust',
                'Scala',
                'Swift'
                ]
    mission =  sys.argv[1]
    model = sys.argv[2]
    for language in language_list:
        input_file = f'data/raw_data/{mission}/{language}.jsonl'
        output_file = f'data/chat_result/{mission}/{model}/{language}.jsonl'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(input_file, 'r',encoding='utf-8') as file:
            data = [json.loads(line) for line in file]
        for index,item in enumerate(data):
            data[index]['llm_response'] = chat(item['instruction'],model)
        with open(output_file, 'w',encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')         