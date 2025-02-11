import json
import shutil
import os
from excute import excute
from units.extract_code import extract_code_block
import sys

def evaluate_answer(user_answer, correct_answers,mode):
    if mode == True: #没有按照格式返回
        user_answers = []
        if "A" in user_answer:
            user_answers.append("A")
        if "B" in user_answer:
            user_answers.append("B")
        if "C" in user_answer:
            user_answers.append("C")
        if "D" in user_answer:
            user_answers.append("D")
        
    else:   
        user_answers = user_answer.strip().upper().replace("[","").replace("]","").replace("\"","").split(',')
        user_answers = [ans.strip() for ans in user_answers]
        #print(user_answers)
    # print(user_answers)
    return set(user_answers) == set(correct_answers)

def check_right(file,language):
    with open(file,"r",encoding='utf-8') as f:
        dataset = []
        for line in f:
            dataset.append(json.loads(line))
    total = len(dataset)
    fail_list = []
    for i,data in enumerate(dataset):
        llm_answer = extract_code_block(data['llm_response'],"Python")
        gt_answer = data["loc_answer"]
        mode = llm_answer == data['llm_response']
        if not evaluate_answer(llm_answer, gt_answer,mode):
            fail_list.append(i+1)
    return fail_list,total
                
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
    model = sys.argv[1]
    mission = "loc"
    output_file = f'data/run_result/{mission}/{model}/info.jsonl'
    os.makedirs(os.path.dirname(f'data/run_result/{mission}/{model}/info.jsonl'), exist_ok=True)
    all_total = 0
    all_fail_num = 0
    for language in language_list:

        file = f'data/chat_result/{mission}/{model}/{language}.jsonl'
        fail_list,total = check_right(file,language)
        all_total += total
        all_fail_num += len(fail_list)
        print(f"language:{language},total:{total},wrong:{len(fail_list)},rate:{(total-len(fail_list))/total}")
        info = {'language':language,'fail_list':fail_list,'fail_num':len(fail_list),'total':total}
        with open(output_file, 'a') as f:
            json.dump(info, f)    
            f.write('\n')
    
    print(f"all_total:{all_total},all_wrong:{all_fail_num},rate:{(all_total-all_fail_num)/all_total}")