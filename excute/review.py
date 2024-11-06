import os
import sys
import json

def check_right(file):
    with open(file,"r",encoding='utf-8') as f:
        dataset = []
        for line in f:
            dataset.append(json.loads(line))
    fail_list = []
    total = 0
    for i,data in enumerate(dataset):
        total += 1
        llm_ans = data['fix_code']
        
        if  'A' in llm_ans:
            fix_code = 'A'
        elif 'B' in llm_ans:
            fix_code = 'B'
        if fix_code != data['choice_answer']:
            fail_list.append(i+1)
    return fail_list,total    
    
if __name__ == '__main__':
    language_list = [
                'C',
                'Clisp',
                'CPP',
                'Go',
                'Java',
                'JavaScript',
                'Julia',
                'Pascal',
                'PHP',
                'Python',
                'R',
                'Ruby',
                'Rust',
                'Scala',
                'Swift',
                'C#',
                'F#',
                'JSON',
                ]
    model = sys.argv[1]
    mission = 'review'
    total_num = 0
    total_wrong = 0
    info_list = []
    output_file = f'data/run_result/{model}/{mission}/info.jsonl'
    os.makedirs(os.path.dirname(f'data/run_result/{model}/{mission}/info.jsonl'), exist_ok=True)
    for language in language_list:
        file = f'data/chat_result/{model}/{mission}/{language}.jsonl'
        fail_list,total = check_right(file)
        info = {'language':language,'fail_list':fail_list,'fail_num':len(fail_list),'total':total}
        info_list.append(info)
        total_num += total
        total_wrong += len(fail_list)
    
    with open(output_file, 'w') as f:
        for info in info_list:
            json.dump(info, f)    
            f.write('\n')
    print(f"total:{total_num},wrong:{total_wrong},rate:{(total_num-total_wrong)/total_num}")