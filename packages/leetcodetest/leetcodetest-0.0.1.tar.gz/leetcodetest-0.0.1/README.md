<div align="center">
    <img src="assets/thumbnail.png" alt="Leetcode Test" />
    <h2>Leetcode Test</h2>
    <p>A package that allows you to test leetcode answers with minimal setup.</p>
    <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome" />
</div>

---

## Installation
```bash
pip3 install leetcodetest
```

## Usage
### 1. Import Leetcodetest:
```python
from leetcodetest import LeetcodeTester
```

### 2. Copy the Solution class:
```python
class Solution:
    def arrayIntoInteger(self, arr):
        return sum(arr)
```

### 3. Specifcy the input and expected output:
```python
LeetcodeTester.test(Solution, givenInput=[1, 2, 3], expectedOutput=6)
```

Ready! Work on your problem and run the file to see your results.

Note: LeetcodeTest automatically finds the method to test your solution, to do so it looks for methods that do not start with _.
You may have only one method which is usually provided by Leetcode. Prefix other methods using _.
```python
# Forbidden
class Solution:
    def my_method(self):
        print("Not OK")
        self.my_method_two()

    def my_method_two(self):
        print("Not OK")

# Correct usage
class Solution:
    def my_method(self):
        print("OK, I am executed by LeetcodeTest")
        self._my_method_two()

    def _my_method_two(self):
        print("OK")
```

## Contributions
Contributions are welcome at any time.

## Maintainers
| Name                                   |
| :------------------------------------- |
| [@Asmeili](https://github.com/Asmeili) |