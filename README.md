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

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "New Application" and give your bot a name.
3. Navigate to the "Bot" tab and click "Add Bot".
4. Under the "Token" section, click "Copy" to copy your bot token and update your `creds.json` file. **Keep this token secret!**
5. In the "Bot Permissions" section, select the necessary permissions (at minimum: "Send Messages", "Connect", and "Speak").
6. Make sure `PRESENCE INTENT` and `MESSAGE CONTENT INTENT` are both turned to on.
7. In the Discord Developer Portal, go to the "OAuth2" tab.
8. In the "Scopes" section, select `bot` and `Administrator`.
9. Copy the generated URL and open it in a new browser tab to invite the bot to your server.
10. Join a voice channel.
11. Use the `!play` command followed by a YouTube URL or search query to start playing music.
12. Use other commands like `!stop`, `!skip`, and `!queue` to control playback and manage the queue.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This bot is for educational purposes only. Please ensure you comply with YouTube's terms of service and respect copyright laws when using this bot.