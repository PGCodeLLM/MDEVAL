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
                 'HTML': 'html',
                 'Markdown': 'md'
                 }

def json2file_fix(line):
    language_type = line['question_id'].split('/')[0]
    question_id = line['question_id'].split('/')[1]
    if language_type == 'F#':
        content = f"{line['llm_response']}\n\n{line['test']}"
        output_file = 'env/F#/MyFsharpApp/Program.fs'
    elif language_type == 'C#':  # C#
        content = f"{line['llm_response']}\n\n{line['test']}"
        output_file = 'env/C#/MyConsoleApp/Program.cs'
    elif language_type == 'Rust':  # C#
        content = f"{line['llm_response']}\n\n{line['test']}"
        output_file = 'env/Rust/rust/src/main.rs'
        # output_file = 'tmp' + '/' + question_id + '.' + extension_dic[language_type]
    elif language_type == 'Go':
        content = f"{line['llm_response']}\n\n{line['test']}"
        output_file = 'env/Go/go/' + question_id+'_test' + \
            '.' + extension_dic[language_type]
    
    elif language_type in ['JSON', 'HTML', 'Markdown']:
        output_file = ""
        pass

    elif language_type == 'PHP':
        content = f"<?php\nassert_options(ASSERT_ACTIVE, 1);\nassert_options(ASSERT_BAIL, 1);\n\n{line['llm_response']}\n\n{line['test']}"
        output_file = 'env/tmp' + '/' + question_id + \
            '.' + extension_dic[language_type]
    else:
        content = f"{line['llm_response']}\n\n{line['test']}"
        # 写入文件
        output_file = 'env/tmp' + '/' + question_id + \
            '.' + extension_dic[language_type]

    if language_type not in ['HTML', 'Markdown', 'JSON']:
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
        data['llm_response'] = extract_code_block(data['llm_response'],language)
        if language == 'C' and '#include <assert.h>' not in data['llm_response']:
            data['llm_response'] = '#include <assert.h>\n' + data['llm_response']
        if (language == 'CPP' and '#include<cassert>' not in data['llm_response']):
            data['llm_response'] = '#include <cassert>\n' + data['llm_response']
        if (language == 'C#' and 'using System;' not in data['llm_response']):
            data['llm_response'] = 'using System;\nusing System.Collections.Generic;\nusing System.Diagnostics;\n' + data['llm_response']
        if (language == 'F#' and 'open System' not in data['llm_response']):
            data['llm_response'] = 'open System\n' + data['llm_response']
        if (language == 'Swift' and 'import Foundation' not in data['llm_response']):
            data['llm_response'] = 'import Foundation\n' + data['llm_response']
        if (language == 'Go' and '"github.com/stretchr/testify/assert"' not in data['llm_response']):
            #print(i+1)
            if "package main" not in data['llm_response']:
                data['llm_response'] = 'package main\n\nimport (\n\t"testing"\n\t"github.com/stretchr/testify/assert"\n)\n' + data['llm_response']
            elif 'import (\n' not in data['llm_response']:
                data['llm_response'] = 'package main\n\nimport (\n\t"testing"\n\t"github.com/stretchr/testify/assert"\n)\n' + data['llm_response'].split('package main')[1]
            else:
                tmp_data = data['llm_response'].split('import (\n')
                if len(tmp_data) == 2:
                    data['llm_response'] = tmp_data[0] + '\nimport (\n\t"testing"\n\t"github.com/stretchr/testify/assert"\n' + tmp_data[1]
        output_file,language,_ ,file_ext= json2file_fix(data)
        if (not excute(language, output_file, data['question_id'], 'env/tmp',data)):
            fail_list.append(i+1)
            print(f"{language} fix error: {i+1}")
    print(f"{language} pass rate: {1-len(fail_list)/total}")
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
    mission =  sys.argv[1]
    model = sys.argv[2]
    input_dir = f'data/chat_result/{model}/{mission}'
    output_file = f'data/eval_result/{model}/{mission}/evaluation_results.jsonl'

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    all_fail = 0
    all_total = 0
    for language in language_list:
        print(f"start check {model}:{language}")
        file = f'{input_dir}/{language}.jsonl'

        # Skip languages that don't have corresponding files
        if not os.path.exists(file):
            print(f"Skipping {language} - no input file found at {file}")
            continue

        fail_list,total = check_excute(file,language)
        all_fail += len(fail_list)
        all_total += total
        info = {'language':language,'fail_list':fail_list,'fail_num':len(fail_list),'total':total}
        with open(output_file, 'a') as f:
            json.dump(info, f)
            f.write('\n')
    print(f"all pass rate: {1-all_fail/all_total}")
