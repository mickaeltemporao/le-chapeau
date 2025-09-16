import random

def process_emails(input_file, output_file):
    with open(input_file, 'r') as f:
        emails = f.readlines()

    users = []
    for email in emails:
        email = email.strip()
        if not email:
            continue
        group = random.choice(['a', 'b'])
        users.append(f"{email},{group}\n")

    with open(output_file, 'w') as f:
        f.writelines(users)

# Example usage:
input_file = 'students.csv'  # Replace with your input file
output_file = 'users_spb.txt'  # Replace with your desired output file
process_emails(input_file, output_file)
