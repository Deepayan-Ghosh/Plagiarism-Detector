# Plagiarism Detector
This detector takes two files or two text segments and compares them for matching portions of text. The files can be uploaded in the GUI or text segments can be pasted or written in the text fields and then upon pressing `compare` button the result is displayed in a top-level window. The results show the percentage of plagiarism in each text, and matching portions are highlighted in red.

## Algorithms and Data-Structure used
1. Rabin-Karp string matching algorithm slightly modified to work with words rather than each letter of a string. List of possible matches is obtained using this.
2. Bloom filters with 0.5% false positive rate is used. They help in identifying possible matches..
3. Aho-Corasick algorithm is used for exact matching.

## How it works?
Given two text files, one of them is considered the pattern string while the other as the source string. 
1. Each file is split into consecutive phrases of 3 words. Say, for example, we have a file whose words are `A B C D E` where `A,B,C,D,E` are individual words. Then after splitting we will have a list of `['A B C', 'B C D', 'C D E']` that is phrases of three words each.
2. The hash value of each word is the sum of the ascii values of each letter of the word, and is calculated seperately in a list. The hash values of each word is pre-computed  and stored in seperate list while splitting the file into phrases.
3. Then the hash value of a phrase is calculated as `x1 + x2*a + x3*a^2` where `x1,x2,x3` are the hash values of three words in a phrase, and `a` represents a prime number. Seven such hash values using seven different prime numbers are calculated for the same phrase, and then they are mapped to a bloom filter.
4. After all the phrases of one file is finished, the same is done for the other file. Here, rather than simply mapping the hash values to a bloom filter, the hash values are checked against the previous bloom filter whether they are already set or not. If they are already set then a match is found and the matching values are mapped to a second bloom filter.
5. After step 4, we have those phrases that can produce possible matches from the second file but we have the whole first file. Unlike regular Rabin-Karp where we have a single pattern, here we have multiple patterns which are to be checked for exact match against an entire file(first file). So to reduce the search space for exact matching using aho-corasick, a second round of filtering is done on the source file phrases against the second bloom filter. If a match is present, the phrase is allowed else the phrase is deleted. The idea is that the phrases in source file which do not show a match against the second bloom filter should not be considered for the exact match. 
6. After step 5, we have only those phrases from the first file which have a high chance of producing matches. So, after this exact matching is done using aho-corasick algorithm. (pyahocorasick module has been used for efficient implementation).
