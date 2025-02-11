import contextlib
import signal
import subprocess as sp
import json
import os
import time
import markdown
import filecmp
import traceback
import shutil 

# from .safe_subprocess import run
import safe_subprocess as subprocess
from bs4 import BeautifulSoup
timeout = 30

@contextlib.contextmanager
def time_limit(seconds: float):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.setitimer(signal.ITIMER_REAL, seconds)
    signal.signal(signal.SIGALRM, signal_handler)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)

class TimeoutException(Exception):
    pass

def excute(language_type, path, task_id, temp_dir,data)->bool:
    if language_type == "python" or language_type == "Python":
        try:
            exec_res = None
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['python', path])
                #print(task_id)
                if run_result.exit_code != 0:
                    print(task_id)
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    return False
                else:
                    # print(task_id)
                    # print("pass")
                    return True
        except TimeoutException:
            print("time out")
            return False
    elif language_type == "Clisp":
        try:
            exec_res = None
            with time_limit(timeout):
                run_result = subprocess.run(
                    ["sbcl", "--script", path])
                # print(task_id)
                if run_result.exit_code != 0:
                    print(f"{task_id}:fail")
                    #print(run_result.stderr)
                    return False
                else:
                    print(f"{task_id}:pass")
                    return True
        except TimeoutException:
            print("time out")
            return True
    elif language_type == "C":
        try:
            module_name = os.path.join(temp_dir, path.split("/")[1].split(".")[0])
            compile_command = ['gcc', '-o', module_name, path, '-lm', '-fsanitize=address','-pthread']
            # print(module_name)
            run_test_command = [module_name]
            compile_result = subprocess.run(
                compile_command)

            if compile_result.exit_code != 0 or 'warning' in compile_result.stderr:
                #print("编译失败:", compile_result.stderr)
                return False
            else:   
                #print("编译成功")
                with time_limit(timeout):
                    # 运行测试
                    run_test_result = subprocess.run(
                        run_test_command)

                    # 输出测试结果
                    # print("测试结果:\n", run_test_result.stdout)

                    # 判断测试是否成功
                    if run_test_result.exit_code != 0:
                        #print("测试执行失败")
                        #print(run_test_result.stderr)
                        return False
                    elif 'failed' in run_test_result.stdout:
                        #print("error 测试执行失败")
                        return False
                    else:
                        #print("测试执行成功")
                        return True
        except TimeoutException:
            #print("time out")
            return False
    elif language_type == "CPP":
        try:
            # print(path, path.split("/")[-1].split(".")[0])
            module_name = os.path.join(temp_dir, path.split("/")[-1].split(".")[0])
            #compile_command = ['g++', '-g', '-std=c++11', '-o', module_name, path]
            compile_command = ['g++', '-g', '-std=c++11', '-o', module_name, path,"-pthread","-fsanitize=address"]

            # print(module_name)
        
            run_test_command = [module_name]

            # 编译 fortran 程序
            # compile_result = subprocess.run(compile_command)
            compile_result = subprocess.run(compile_command)

            # 检查编译是否成功
            if compile_result.exit_code != 0:
                #print("编译失败:", compile_result.stderr)
                return False
            else:
                #print("编译成功")
                with time_limit(timeout):
                    # 运行测试
                    run_test_result = subprocess.run(run_test_command)
                    output = run_test_result.stdout
                    # for encoding in ['utf-8', 'iso-8859-1', 'gbk']:
                    #     try:
                    #         output = run_test_result.stdout.decode(encoding)
                    #         break
                    #     except UnicodeDecodeError:
                    #         pass
                    # else:
                    #     raise UnicodeDecodeError('无法解码输出')
                    # 输出测试结果
                    # print("测试结果:\n", output)

                    # 判断测试是否成功
                    if run_test_result.exit_code != 0:
                        # print("测试执行失败")
                        # print(output)
                        return False
                    elif 'failed' in output:
                        #print("error 测试执行失败")
                        return False
                    else:
                        #print("测试执行成功")
                        return True
        except TimeoutException:
            #print("time out")
            return False
    elif language_type == "Go":
        ori_path = os.getcwd()
        file_name = path.split('/')[-1]
        #shutil.copy(path, './go/'+file_name)
        #os.chdir('./go')
        os.chdir(os.path.dirname(path))
        try:
            with time_limit(timeout+20):
                run_result = subprocess.run(['go', 'test', file_name])
                if run_result.exit_code != 0:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    os.chdir(ori_path)
                    return False
                elif 'assert()' in  run_result.stderr and 'failed' in run_result.stderr:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    os.chdir(ori_path)
                    return False
                else:
                    #print("pass")
                    os.chdir(ori_path)
                    return True

        except TimeoutException:
            #print("time out")
            os.chdir(ori_path)
        os.chdir(ori_path)
        return False
    elif language_type == "Rust":
        try:
            ori_path = os.getcwd()
            os.chdir(os.path.dirname(path))
            subprocess.run(
                ['rm', '-rf', 'target'])
            with time_limit(timeout+20):
                time.sleep(1)
                run_result = subprocess.run(
                    ['cargo', 'test'])

                # print(task_id)
                # print(run_result)
                if run_result.exit_code != 0:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    time.sleep(1)
                    os.chdir(ori_path)
                    return False
                else:
                    #print("pass")
                    time.sleep(1)
                    os.chdir(ori_path)
                    return True

        except TimeoutException:
            #print("time out") 
            time.sleep(1)
            os.chdir(ori_path) 
            return False
    elif language_type in ["cs", 'C_sharp', 'C#']:
        try:
            # print(path)
            project_path = path[:-11]
            #print('++++++++',project_path)
            with time_limit(timeout*2):
                run_result = sp.run(
                    ["dotnet", "run", "--project", project_path])
                # print(task_id)
                if run_result.returncode != 0:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            #print("time out")
            return False
        finally:
            # 添加清理操作，终止相关进程
            print("kill process")
            subprocess.run(
                ["ps", "aux", "|", "grep", project_path, "|", "awk", "'{print $2}'", "|", "xargs", "kill", "-9"],
            )  
    elif language_type == "F#":
        try:
            project_path = path[:-11]
            print(project_path)
            with time_limit(timeout):
                run_result = sp.run(
                    ["dotnet", "run", "--project", project_path])
                
                #print(task_id)
                if run_result.returncode != 0:
                    print("Run failed. Error message:")
                    print(run_result.stderr)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            print("time out")
            return False
        finally:
            # 添加清理操作，终止相关进程
            print("kill process")
            subprocess.run(
                ["ps", "aux", "|", "grep", project_path, "|", "awk", "'{print $2}'", "|", "xargs", "kill", "-9"],
            )        
    elif language_type == "JavaScript":
        try:
            exec_res = None
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['node', path])
                if run_result.exit_code != 0:
                    # print("\nRun failed. Error message:")
                    # print(run_result.stderr)
                    return False
                elif 'failed' in run_result.stderr:
                    # print("\nRun failed. Error message:")
                    # print(run_result.stderr)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            #print("time out")
            return False
    elif language_type in ["ruby", 'Ruby']:
        try:
            exec_res = None
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['ruby', path])
                # print(task_id)
                # print(run_result)
                if run_result.exit_code != 0:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            #print("time out")
            return False
        
    elif language_type in ["php", "PHP"]:
        try:
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['php', path])
                # print(task_id)
                # print(run_result)
                if run_result.exit_code != 0:
                    # print("\nRun failed. Error message:")
                    # print(run_result.stderr)
                    return False
                elif 'assert()' in run_result.stderr or 'failed' in run_result.stderr or 'Undefined variable' in run_result.stderr:
                    # print("\nRun failed. Error message:")
                    # print(run_result.stderr)
                    return False
                else:
                    # print("pass")
                    return True
        except TimeoutException:
            # print("time out")
            return False
    elif language_type == "Swift":
        try:
            exec_res = None
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['swift', path])
                # print(task_id)
                if run_result.exit_code != 0:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stdout)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            #print("time out")
            return False
    
    elif language_type in ['r', 'R']:
        try:
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['Rscript', path])
                # print(task_id)
                # print(run_result)
                if run_result.exit_code != 0:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            #print("time out")
            return False
        
    elif language_type in ["julia", "Julia"]:
        try:
            exec_res = None
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['julia', path])
                # print(task_id)
                if run_result.exit_code != 0 or 'ERROR' in run_result.stderr:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            #print("time out")
            return False
    elif language_type == "Pascal":
        try:
           
            module_name = os.path.join(temp_dir, path.split("/")[-1].split(".")[0])
            compile_command = ['fpc', path, '-MObjfpc']
            run_test_command = [module_name]
            compile_result = subprocess.run(
                compile_command)

            # 检查编译是否成功
            if compile_result.exit_code != 0:
                #print("编译失败:", compile_result.stdout)
                return False
            else:
                #print("编译成功")
                with time_limit(timeout):
                    # 运行测试
                    run_test_result = subprocess.run(
                        run_test_command)

                    # 输出测试结果
                    # print("测试结果:\n", run_test_result.stdout)

                    # 判断测试是否成功
                    if run_test_result.exit_code != 0:
                        # print("测试执行失败")
                        # print(run_test_result.stderr)
                        return False
                    elif 'failed' in run_test_result.stderr:
                        # print("error 测试执行失败")
                        return False
                    else:
                        # print("测试执行成功")
                        return True
        except TimeoutException:
            print("time out")
            return False
        except:
            # print(traceback.print_exc())
            # print('error')
            return False
    elif language_type in ["scala", "Scala"]:
        try:
            exec_res = None
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['scala', path])
                # print(task_id)
                # print(run_result)
                os.system('rm -rf env/tmp/.bsp')
                os.system('rm -rf env/tmp/.scala-build')
                if run_result.exit_code != 0:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            #print("time out")
            return False
    elif language_type in ["Java", 'java']:
        try:
            exec_res = None
            with time_limit(timeout):
                run_result = subprocess.run(
                    ['java', '-ea', path])
                # print(task_id)
                # print(run_result)
                if run_result.exit_code != 0 or 'warning' in run_result.stderr:
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    return False
                else:
                    #print("pass")
                    return True
        except TimeoutException:
            #print("time out")
            return False
    elif language_type == "JSON":
        try:
            exec_res = None
            with time_limit(timeout):
                if json.loads(data['canonical_solution']) == json.loads(data['llm_response']):
                    #print("\nRun failed. Error message:")
                    #print(run_result.stderr)
                    return True
                else:
                    # print(task_id)
                    # print("pass")
                    return False
        except Exception as e:
            #print("time out")
            return False
    elif language_type == "HTML":
        try:
            exec_res = None
            with time_limit(timeout):
                html1 = data['canonical_solution']
                html2 = data['llm_response']    
                soup1 = BeautifulSoup(html1, 'html5lib')
                # 生成规范化后的HTML字符串
                normalized_html1 = soup1.prettify()
                
                # 解析第二个HTML字符串
                soup2 = BeautifulSoup(html2, 'html5lib')
                # 生成规范化后的HTML字符串
                normalized_html2 = soup2.prettify()
                
                # 比较两个规范化后的HTML字符串
                return normalized_html1 == normalized_html2
        except Exception as e:
            return False
    
    elif language_type == "Markdown":
        def normalize_html(html):
            soup = BeautifulSoup(html, 'html.parser')
            # 去除所有空格和换行符，只保留文本和标签结构
            for tag in soup.find_all(True):
                # 去除多余的空格
                if tag.string:
                    tag.string = tag.string.strip()
            # 生成标准化的HTML
            normalized_html = soup.prettify()
            return normalized_html
        try:
            exec_res = None
            with time_limit(timeout):
                md1 = data['canonical_solution'].replace('# ', '#$').replace(' ', '').replace('#$', '# ')
                md2 = data['llm_response'].replace('# ', '#$').replace(' ', '').replace('#$', '# ')
                html1 = markdown.markdown(md1)
                html2 = markdown.markdown(md2)
    
                normalized_html1 = normalize_html(html1)
                normalized_html2 = normalize_html(html2)
                return normalized_html1 == normalized_html2
        except Exception as e:
            print(e)
            return False