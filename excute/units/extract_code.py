import re
import json
def extract_code_block(code,language):
    language_patterns = {
        "C": r"```c(.*?)```",
        "Python": r"```python(.*?)```",
        "Java": r"```java(.*?)}\n```",
        "CPP": r"```cpp(.*?)```",
        "Go": r"```go(.*?)```",
        'Rust': r"```rust(.*?)```",
        'C#': r"```csharp(.*?)\}\n```",
        'F#': r"```fsharp(.*?)```",
        'JavaScript': r"```javascript(.*?)```",
        'Ruby': r"```ruby(.*?)```",
        'PHP': r"```php(.*?)```",
        'Scala': r"```scala(.*?)}\n```",
        'R': r"```r(.*?)```",
        'Swift': r"```swift(.*?)```",
        'Julia': r"```julia(.*?)```",
        'Pascal': r"```pascal(.*?)```",
        'Clisp': r"```lisp(.*?)```",
        'JSON': r"```json(.*?)```"
        # 添加其他语言类型
    }
    # 获取 CPP 模式
    cpp_pattern = language_patterns.get("CPP")
    
    # 获取 C 模式
    c_pattern = language_patterns.get("C")
    pattern = language_patterns.get(language)
    # 使用正则表达式提取文档字符串
    if language == "CPP":
        docstring_match_cpp = re.search(cpp_pattern, code, re.DOTALL)
        docstring_match_c = re.search(c_pattern, code, re.DOTALL)
        
        if docstring_match_cpp:
            extract_code = docstring_match_cpp.group(1).strip()
        elif docstring_match_c:
            extract_code = docstring_match_c.group(1).strip()
        else:
            extract_code = code
    else:
        if not pattern:
            return code
        docstring_match_1 = re.search(pattern, code, re.DOTALL)
        
        if docstring_match_1:
            extract_code = docstring_match_1.group(1).strip()
        else:
            extract_code = code
    
    if language == "Scala" and extract_code.endswith('\n}'):
        extract_code = extract_code[:-1]
        
    return extract_code

if __name__ == "__main__":
    input_file = '/root/McEval/data/result/bug/dpsk/Clisp.jsonl'
    with open (input_file, "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]
        
    for i, data in enumerate(dataset):
        dataset[i]["fix_code"] = extract_code_block(data["fix_code"], "Clisp")
    
    with open(input_file, "w", encoding="utf-8") as f:
        for data in dataset:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")