# Extra Plugins For [YukkiMusic](https://github.com/TheTeamVivek/YukkiMusic)

## Introduction

This repository contains extra plugins for the YukkiMusic bot, which enhance its functionalities and provide additional features. These plugins are designed to work seamlessly with the YukkiMusic bot and can be easily integrated into your existing setup.

## Deployment for [YukkiMusic](https://github.com/TheTeamVivek/YukkiMusic)

### 🚀 Heroku Deployment

Click the button below to deploy Yukki Music Bot on Heroku!
If you encounter any error like "failed to app creation", then fork and deploy.

[![Deploy To Heroku](https://img.shields.io/badge/Deploy%20To%20Heroku-teal?style=for-the-badge&logo=heroku)](https://dashboard.heroku.com/new?template=https://github.com/TheTeamVivek/YukkiMusic)

### 🔧 VPS Deployment

1. Get your [Necessary Variables](https://github.com/TheTeamVivek/YukkiMusic/blob/master/sample.env)
2. Clone the repo: `git clone https://github.com/TheTeamVivek/YukkiMusic && cd YukkiMusic`
3. Set up by: `bash setup`
4. Install tmux to keep running your bot when you close the terminal by: `sudo apt install tmux && tmux`
5. Finally, run the bot by: `python3 -m YukkiMusic`
6. To exit from tmux session: Press `Ctrl+b` and then `d`

For more help, check out [YukkiMusic](https://github.com/TheTeamVivek/YukkiMusic).

## Plugins Overview

This repository includes various plugins that extend the capabilities of the YukkiMusic bot. These plugins utilize the `app` client (Pyrogram), `logger` (initialized client of logging), and `utils` (utility functions) without needing to import them explicitly.

### Example Usage

You can use the attributes and functions provided by `utils.py` directly in your plugins. Here are some examples:

These are some attributes of [`utils`](https://github.com/TheTeamVivek/Extra-Plugin/blob/master/utils.py)
- `utils.get_image(cid)`
- `utils.save_couple(cid, date, couple, img)`
- `utils.set_welcome(chat_id, message, raw_text, file_id)`

You also can use the `app` That is Pyrogram Client without importing and same as with `logger` for logging purposes like logger.info("Hello World")

You can also leverage the dynamic attributes added in [`YukkiMusic/core/bot.py`](https://github.com/TheTeamVivek/YukkiMusic/blob/master/YukkiMusic/core/bot.py) to enhance your plugins.

## Contributing

We welcome contributions from the community. If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear and concise messages.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## License

This project is licensed under the [MIT License](https://github.com/TheTeamVivek/Extra-Plugin/blob/master/LICENSE).

## Credits

Special thanks to all the contributors and the open-source community for their support and contributions.

---

For more information and updates, visit the [YukkiMusic](https://github.com/TheTeamVivek/YukkiMusic) repository.
