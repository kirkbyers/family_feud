# Family Feud Game

This project is a command-line implementation of a Family Feud-style game using Python and the Anthropic API. It generates subjects and related items, allows players to guess the items, and keeps track of scores.

## Features

- Randomly generates game subjects and related items using the Anthropic API
- Allows players to input a custom subject or use a randomly generated one
- Judges player guesses using AI
- Assigns scores to items and tracks player score
- Provides a fun, interactive Family Feud experience in the command line

## Prerequisites

- Docker (optional, for containerized deployment)
- Anthropic API key

## Usage

To run the game using Docker:

1. Build the Docker image:
   ```
   docker build -t family-feud-game .
   ```

2. Run the container:
   ```
   docker run -it --env ANTHROPIC_API_KEY='your_api_key_here' family-feud-game
   ```

## How to Play

1. When prompted, enter a subject for the game or press Enter for a random subject.
2. Try to guess the top answers related to the subject.
3. You have three wrong guesses before the game ends.
4. The game will provide feedback on your guesses and keep track of your score.
5. The game ends when you've guessed all items or used up all your wrong guesses.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
