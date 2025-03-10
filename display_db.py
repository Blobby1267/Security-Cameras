import sqlite3

def print_face_data():
    conn = sqlite3.connect('facial_data.db')
    c = conn.cursor()
    
    # Query to get all face data from the face_data table
    c.execute('SELECT * FROM face_data')
    rows = c.fetchall()

    # Check if the database contains any data
    if not rows:
        print("No face data found in the database.")
        conn.close()
        return

    # Print the header
    print(f"{'Face ID':<10}{'Timestamp':<20}{'Landmarks (sample)':<50}")
    print("-" * 80)

    # Print all rows in the database
    for row in rows:
        landmarks = row[2].split(',')
        landmarks_sample = landmarks[:10]  # Show only a sample of the first 10 landmarks for brevity
        print(f"{row[0]:<10}{row[1]:<20}{' '.join(landmarks_sample)}...")  # Display sample of landmarks

    conn.close()

# Call the function to print the face data
print_face_data()