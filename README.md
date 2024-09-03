# PiratesAhoy Discord Bot

PiratesAhoy is a Discord bot that brings the joy of music to your server! With easy-to-use commands, you can play, queue, and manage songs from YouTube directly in your voice channels.

## Features

- Play music from YouTube links or search queries
- Queue system for multiple songs
- Interactive song selection from search results
- Basic playback controls (stop, skip)
- Queue management and display
- Auto-Deletion of Bot-User interactions after 60 seconds to keep channels tidy.
- All messages are sent silently to not spam notifications.

## Commands

- `!play <query or URL>`: Play a song or add it to the queue
- `!stop`: Stop the current playback
- `!skip`: Skip the current song
- `!queue`: Display the current song queue

## Setup

1. Clone this repository to your local machine.

2. Create a virtual environment:

   **Linux/macOS:**
   ```
   python3 -m venv venv
   ```

   **Windows:**
   ```
   python -m venv venv
   ```

3. Make sure FFMPEG is installed

   **Linux**
   ```
   sudo apt install ffmpeg
   ```

   **macOS**
   ```
   brew install ffmpeg
   ```

   **Windows**
   Download from:
   ```
   https://ffmpeg.org/download.html
   ```

4. Activate the virtual environment:

   **Linux/macOS:**
   ```
   source venv/bin/activate
   ```

   **Windows:**
   ```
   venv\Scripts\activate
   ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Create a `creds.json` file in the root directory with your Discord bot token:
   ```json
   {
     "token": "YOUR_BOT_TOKEN_HERE"
   }
   ```

7. Run the bot:
   ```
   python bot.py
   ```

## Usage

1. Invite the bot to your Discord server 
`https://discord.com/oauth2/authorize?client_id=1279990574425968642&permissions=8&integration_type=0&scope=bot`
2. Join a voice channel in your server.
3. Use the `!play` command followed by a YouTube URL or search query to start playing music.
4. Enjoy your tunes!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This bot is for educational purposes only. Please ensure you comply with YouTube's terms of service and respect copyright laws when using this bot.