import csv
import random
import time

# Create a file called fake_traffic.csv in our project folder
with open("fake_traffic.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write the headers
    writer.writerow(["Timestamp", "Packet_Size_Bytes"])

    # Start time: right now
    start_time = int(time.time())

    print("Generating 10 minutes of network traffic data...")

    # Loop through 600 seconds (10 minutes)
    for i in range(600):
        timestamp = start_time + i

        # Most of the time, traffic is normal (between 100 and 1500 bytes)
        if 200 <= i <= 230:
            # HIDING A SUSTAINED SPIKE: Between seconds 200 and 230, traffic goes crazy!
            packet_size = random.randint(80000, 95000)
        else:
            # Normal everyday traffic
            packet_size = random.randint(100, 1500)

        writer.writerow([timestamp, packet_size])

print("Success! 'fake_traffic.csv' has been created.")
