using System;
using System.Collections.Generic;
using System.Diagnostics;

class Program
{
   
   static string CopySubstringFromIndex(string input, int startIndex)

{
    if (startIndex >= input.Length)
    {
        return "";
    }
    return input.Substring(startIndex, input.Length);
}

static void check()
    {
        Debug.Assert(CopySubstringFromIndex("Hello World", 6) == "World");
        Debug.Assert(CopySubstringFromIndex("Example", 3) == "mple");
        Debug.Assert(CopySubstringFromIndex("Short", 10) == "");
        Debug.Assert(CopySubstringFromIndex("AnotherExample", 0) == "AnotherExample");
        Debug.Assert(CopySubstringFromIndex("Test", 4) == "");
        Debug.Assert(CopySubstringFromIndex("", 0) == "");
        Debug.Assert(CopySubstringFromIndex("LastOne", 7) == "");

    }
static void Main(){
    check();
}
}