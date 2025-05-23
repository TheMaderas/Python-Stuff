"""
Secure password generator with customizable options.
This script allows generating random passwords with different levels of complexity.
"""
import random
import string
import argparse

def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_special=True):
    """
    Generates a random password based on the provided parameters.
    
    Args:
        length (int): Password length
        use_uppercase (bool): Include uppercase letters
        use_lowercase (bool): Include lowercase letters
        use_digits (bool): Include numbers
        use_special (bool): Include special characters
        
    Returns:
        str: The generated password
    """
    characters = ""
    
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%&*()_+-=[]{}|;:,.<>?/§€£"
    
    if not characters:
        characters = string.ascii_lowercase  # Default: use at least lowercase letters
    
    password = "".join(random.choice(characters) for _ in range(length))
    return password

def main():
    parser = argparse.ArgumentParser(description='Secure Password Generator')
    parser.add_argument('-l', '--length', type=int, default=12, help='Password length')
    parser.add_argument('--no-upper', action='store_false', dest='use_uppercase', 
                        help='Do not use uppercase letters')
    parser.add_argument('--no-lower', action='store_false', dest='use_lowercase',
                        help='Do not use lowercase letters')
    parser.add_argument('--no-digits', action='store_false', dest='use_digits',
                        help='Do not use numbers')
    parser.add_argument('--no-special', action='store_false', dest='use_special',
                        help='Do not use special characters')
    parser.add_argument('-n', '--num-passwords', type=int, default=1,
                        help='Number of passwords to generate')
    
    args = parser.parse_args()
    
    print('\n' + '='*50)
    print(' SECURE PASSWORD GENERATOR ')
    print('='*50)
    
    for i in range(args.num_passwords):
        password = generate_password(
            args.length, 
            args.use_uppercase, 
            args.use_lowercase,
            args.use_digits,
            args.use_special
        )
        print(f'Password {i+1}: {password}')
    
    print('='*50 + '\n')

if __name__ == "__main__":
    main()
