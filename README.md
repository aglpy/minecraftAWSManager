# minecraftAWSManager
Manager for automated minecraft server using AWS services

## How to use

- This code is ready to use as a lambda function in AWS
- The lambda function requires a EventBridge trigger to execute the function periodically (every 5 minutes is fine)
- It is required a DynamoDB table called minecraft_server_players with keys "timestamp" and "players" to store the time and the number of players in the minecraft server in each timestamp, better to be initialized with random coherent data
- An EC2 instance is requried with a minecraft server ready to launch, the port should be updated in lambda function
