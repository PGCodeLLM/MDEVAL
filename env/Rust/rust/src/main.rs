fn max_prime_factor_in_list(numbers: &[i32]) -> i32
{
    let mut max_prime = -1;
    let mut result = -1;

    for &num in numbers {
        let prime_factor = largest_prime_factor(num);
        if prime_factor > max_prime {
            max_prime = prime_factor;
            result = num;
        }
    }

    result
}

fn largest_prime_factor(mut n: i32) -> i32 
{
    let mut max_prime = -1;

    // Divide n by 2 until it becomes odd
    while n % 2 == 0 {
        max_prime = 2;
        n /= 2;
    }

    // n must be odd at this point, so a skip of 2 (i += 2) can be used
    for i in (3..=(n as f64).sqrt() as i32).step_by(2) {
        while n % i == 0 {
            max_prime = i;
            n /= i;
        }
    }

    // Handle the case when n is a prime number greater than 2
    if n > 2 {
        max_prime = n;
    }

    max_prime
}

#[cfg(test)]
mod tests {
    use super::*;
 
    #[test]
    fn main() {
        assert_eq!(max_prime_factor_in_list(&[36, 38, 40, 42]), 38);
        assert_eq!(max_prime_factor_in_list(&[10, 15, 21, 22]), 22);
        assert_eq!(max_prime_factor_in_list(&[7, 11, 13, 19]), 19);
        assert_eq!(max_prime_factor_in_list(&[2, 3, 5, 7]), 7);
    }
    

}