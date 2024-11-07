using System;
using System.Collections.Generic;

class Program
{
    static bool HasCloseElements(List<double> numbers, double threshold)
    {
        for (int i = 0; i < numbers.Count - 1; i++)
        {
            for (int j = i + 1; j < numbers.Count; j++)
            {
                double distance = Math.Abs(numbers[i] - numbers[j]);
                if (distance < threshold)
                {
                    return true;
                }
            }
        }
        return false;
    }

static void check()
    {

        // Test cases
        Console.WriteLine(HasCloseElements(new List<double> { 1.0, 2.0, 3.9, 4.0, 5.0, 2.2 }, 0.3) == true);
        Console.WriteLine(HasCloseElements(new List<double> { 1.0, 2.0, 3.9, 4.0, 5.0, 2.2 }, 0.05) == false);
        Console.WriteLine(HasCloseElements(new List<double> { 1.0, 2.0, 5.9, 4.0, 5.0 }, 0.95) == true);
        Console.WriteLine(HasCloseElements(new List<double> { 1.0, 2.0, 5.9, 4.0, 5.0 }, 0.8) == false);
        Console.WriteLine(HasCloseElements(new List<double> { 1.0, 2.0, 3.0, 4.0, 5.0, 2.0 }, 0.1) == true);
        Console.WriteLine(HasCloseElements(new List<double> { 1.1, 2.2, 3.1, 4.1, 5.1 }, 1.0) == true);
        Console.WriteLine(HasCloseElements(new List<double> { 1.1, 2.2, 3.1, 4.1, 5.1 }, 0.5) == false);
    }
static void Main(){
    check();
}
}