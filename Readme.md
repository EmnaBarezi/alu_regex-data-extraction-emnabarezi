# ALU Regex Data Extraction

This is a simple project that extracts data from messy text using Python and regex.

It can find:

- Emails (like emnaba17@gmail.com)  
- URLs  (like https://www.shiptrack.com/tracking/TB123456789) the link in output
- Phone numbers (like 123-456-7890)  
- Credit card numbers (masked in the output)  
- Times (like 8:30 AM or 20:30)  
- Currency amounts (like $12.99)


# How to Use

1. Put your text in a file called "input.txt" in the same folder as the Python script.  
2. Run the script using Python:
3. The results will be saved automatically in "output.json".  
4. Sensitive data like emails and credit cards are masked in the output for safety.


# Files in the Project
We have:

- Regex extractor.py (Souce code) for main Python script  
- input.txt for the sample text input  
- output.json (Sample output) for results after running the script  
- README.md this file with the explainations


# Notes / Security Awareness

- The program checks the input for unsafe things like 'script' tags or suspicious paths.  
- Invalid or malicious input is ignored.  
- Only valid patterns are extracted.  




