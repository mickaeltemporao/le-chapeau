import random

def process_emails(input_file, output_file):
    with open(input_file, 'r') as f:
        emails = f.readlines()

    users = []
    for email in emails:
        email = email.strip()
        if not email:
            continue
        username = email.split('@')[0]
        group = random.choice(['a', 'b'])
        users.append(f"{username},{group}\n")

    with open(output_file, 'w') as f:
        f.writelines(users)

# Example usage:
input_file = 'raw-sample.txt'  # Replace with your input file
output_file = 'users.txt'  # Replace with your desired output file
process_emails(input_file, output_file)
