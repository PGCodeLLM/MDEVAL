import json
import shutil
import os
from excute import excute
from units.extract_code import extract_code_block
import sys

extension_dic = {'Clisp': 'lisp',
                 'Emacs Lisp': "el", 'Elixir': 'exs', 'Racket': 'rkt', 'Scheme': 'scm', 'Haskell': 'hs', 'Shell': 'sh', 'PowerShell': 'ps1', 'Swift': 'swift', 'Perl': 'pl', 'Tcl': 'tcl',
                 'Python': 'py',
                 'sql': 'py',
                 'Julia': 'jl',
                 'coffee': 'coffee',
                 'kotlin': 'kts',
                 'PHP': 'php',
                 'R': 'R',
                 'Ruby': 'rb',
                 'Java': 'java',
                 'C#': 'cs',
                 'fortran': 'f95',
                 'Rust': 'rs',
                 'Scala': 'scala',
                 'dart': 'dart',
                 'groovy': 'groovy',
                 'C': 'c',
                 'CPP': 'cpp',
                 'Go': 'go',
                 'JavaScript': 'js',
                 'TypeScript': 'ts',
                 'VimScript': 'vim',
                 'Lua': 'lua',
                 'Pascal': 'pas',
                 'F#': 'fs',
                 'JSON': 'json',
                 }

def json2file_fix(line):
    language_type = line['question_id'].split('/')[0]
    question_id = line['question_id'].split('/')[1]
    if language_type == 'F#':
        content = f"{line['fix_code']}\n\n{line['test']}"
        output_file = 'env/C#/MyFsharpApp/Program.fs'
    elif language_type == 'C#':  # C#
        content = f"{line['fix_code']}\n\n{line['test']}"
        output_file = 'env/F#/MyConsoleApp/Program.cs'
    elif language_type == 'Rust':  # C#
        content = f"{line['fix_code']}\n\n{line['test']}"
        output_file = 'env/Rust/rust/src/main.rs'
        with open('./tmp/' + question_id + '.' + extension_dic[language_type], 'w') as f:
            f.write(content)
        # output_file = 'tmp' + '/' + question_id + '.' + extension_dic[language_type]
    elif language_type == 'Go':
        content = f"{line['fix_code']}\n\n{line['test']}"
        output_file = 'env/Go/go/' + question_id+'_test' + \
            '.' + extension_dic[language_type]
    
    elif language_type == 'JSON':
        question_id = line['question_id'].split('/')[1]
        output_file = f'tmp/{question_id}.json'
    elif language_type == 'PHP':
        content = f"<?php\nassert_options(ASSERT_ACTIVE, 1);\nassert_options(ASSERT_BAIL, 1);\n\n{line['fix_code']}\n\n{line['test']}"
        output_file = 'env/tmp' + '/' + question_id + \
            '.' + extension_dic[language_type]
    else:
        content = f"{line['fix_code']}\n\n{line['test']}"
        # 写入文件
        output_file = 'env/tmp' + '/' + question_id + \
            '.' + extension_dic[language_type]

    if language_type not in ["AWK", 'HTML', 'Markdown', 'JSON']:
        with open(output_file, 'w') as f:
            f.write(content)
    return output_file, language_type, line['question_id'],extension_dic[language_type]

def check_excute(file,language):
    # 执行检查单个语言
    with open(file,"r",encoding='utf-8') as f:
        dataset = []
        for line in f:
            dataset.append(json.loads(line))
    total = len(dataset)
    fail_list = []
    for i , data in enumerate(dataset):
        data['fix_code'] = extract_code_block(data['fix_code'],language)
        if language == 'C' and '#include <assert.h>' not in data['fix_code']:
            data['fix_code'] = '#include <assert.h>\n' + data['fix_code']
        if (language == 'CPP' and '#include<cassert>' not in data['fix_code']):
            data['fix_code'] = '#include <cassert>\n' + data['fix_code']
        if (language == 'C#' and 'using System;' not in data['fix_code']):
            data['fix_code'] = 'using System;\nusing System.Collections.Generic;\nusing System.Diagnostics;\n' + data['fix_code']
        if (language == 'F#' and 'open System' not in data['fix_code']):
            data['fix_code'] = 'open System\n' + data['fix_code']
        if (language == 'Swift' and 'import Foundation' not in data['fix_code']):
            data['fix_code'] = 'import Foundation\n' + data['fix_code']
        output_file,language,_ ,file_ext= json2file_fix(data)
        if (not excute(language, output_file, data['question_id'], 'env/tmp',data)):
            print(f"{language} fix error: {i+1}")
    print(f"{language} pass rate: {1-len(fail_list)/total}")
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
                'JSON'
                ]
    mission =  sys.argv[1]
    model = sys.argv[2]
    output_file = f'data/run_result/{model}/{mission}/info.jsonl'
    os.makedirs(os.path.dirname(f'data/run_result/{model}/{mission}/info.jsonl'), exist_ok=True)
    for language in language_list:
        file = f'data/chat_result/{model}/{mission}/{language}.jsonl'
        fail_list,total = check_excute(file,language)
        info = {'language':language,'fail_list':fail_list,'fail_num':len(fail_list),'total':total}
        with open(output_file, 'a') as f:
            json.dump(info, f)    
            f.write('\n')