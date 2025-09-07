# Initialize a dictionary to hold the counts
group_counts = {}

# Open the file and read line by line
with open('users.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line:  # Ensure the line is not empty
            # Split the line by commas and get the last element
            last_part = line.split(',')[-1]
            # The group is the last character of the last part
            group = last_part[-1]
            # Increment the count for the group
            group_counts[group] = group_counts.get(group, 0) + 1

# Calculate the total number of entries
total = sum(group_counts.values())

# Calculate the proportions
group_proportions = {
    group: count/total for group, count in group_counts.items()
}

# Print the results
print("Group counts:", group_counts)
print("Group proportions:", group_proportions)
