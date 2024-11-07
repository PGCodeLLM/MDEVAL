fn has_close_elements(numbers: Vec<f32>, threshold: f32) -> bool {
    for i in 0..numbers.len() {
        for j in (i + 1)..numbers.len() {
            let distance: f32 = (numbers[i] - numbers[j]).abs();
            if distance < threshold {
                return true;
            }
        }
    }
    return false;
}

#[cfg(test)]
 mod tests {
  use super::*;
 
  #[test]
  fn test_has_close_elements() {
  assert_eq!(has_close_elements(vec![11.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3), true);
  assert_eq!(has_close_elements(vec![1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05), false);
  assert_eq!(has_close_elements(vec![1.0, 2.0, 5.9, 4.0, 5.0], 0.95), true);
  assert_eq!(has_close_elements(vec![1.0, 2.0, 5.9, 4.0, 5.0], 0.8), false);
  assert_eq!(has_close_elements(vec![1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1), true);
  assert_eq!(has_close_elements(vec![1.1, 2.2, 3.1, 4.1, 5.1], 1.0), true);
  assert_eq!(has_close_elements(vec![1.1, 2.2, 3.1, 4.1, 5.1], 0.5), false);
  }
 
 }