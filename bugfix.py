from typing import List
# 1. Count and Say
def count_and_say(n: int) -> str:
    if n == 1:
        return "1"
    prev_term = count_and_say(n - 1)
    result = []
    i = 0
    while i < len(prev_term):
        count = 1
        while i + 1 < len(prev_term) and prev_term[i] == prev_term[i + 1]:
            i += 1
            count += 1
        result.append(str(count) + prev_term[i])
        i += 1
    return "".join(result)
    
# 2. ZigZag Conversion
def convert(s: str, numRows: int) -> str:
    if numRows == 1 or numRows >= len(s):
        return s
    res = [''] * numRows
    index, step = 0, 1
    for char in s:
        res[index] += char
        if index == 0:
            step = 1
        elif index == numRows - 1:
            step = -1
        index += step
    return "".join(res)

# 3. Add Binary
def add_binary(a: str, b: str) -> str:
    if not a:
        return b
    if not b:
        return a
    if a[-1] == '1' and b[-1] == '1':
        return add_binary(add_binary(a[:-1], b[:-1]), '1') + '0'
    elif a[-1] == '0' and b[-1] == '0':
        return add_binary(a[:-1], b[:-1]) + '0'
    else:
        return add_binary(a[:-1], b[:-1]) + '1'
        
# 4. Reverse Words in a String III
def reverse_words(s: str) -> str:
    def reverse_word(word: str) -> str:
        if not word:
            return word
        return word[-1] + reverse_word(word[:-1])
    return ' '.join(map(reverse_word, s.split()))

# 5. Unique Email Addresses
def num_unique_emails(emails: List[str]) -> int:
    def process_email(email: str) -> str:
        local, domain = email.split('@')
        local = local.split('+')[0].replace('.', '')
        return local + '@' + domain
    return len(set(map(process_email, emails)))

emails = ["test.email@gmail.com", "test.e.mail@gmail.com", "test+email@gmail.com"]
print(num_unique_emails(emails))
s = "Let's take LeetCode contest"
print(reverse_words(s))
a = "1101"
b = "1011"
print(add_binary(a, b))
s = "PAYPALISHIRING"
numRows = 3
print(convert(s, numRows))
n = 5
print(count_and_say(n))