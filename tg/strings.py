default_lang = None

TEXT = {
    "WELCOME": {
        "en": "Welcome {name} 🤠\n\n"
        "🪪 In this bot you can get the id of any group, channel, user or bot\n\n"
        "📤 To use the bot, click on the buttons below and share the chat whose ID you want to know."
        " - In response, the bot will return the ID of the chat you shared\n\n"
        "> 📝 You can get the ID in many other ways. Send the /help command\n\n"
        "> 🤑 Want to donate to me? Send the /donate command\n\n"
        "📢 For updates on the bot subscribe to @TeleServices_Api\n\nBot creator: @TechsCoder 👨‍💻",
    },
    "USER": {"en": "👤 User"},
    "BOT": {"en": "🤖 Bot"},
    "CHANNEL": {"en": "📢 Channel"},
    "GROUP": {"en": "👥 Group"},
    "ID_USER": {"en": "🪪 The ID of {} is: `{}`"},
    "ID_USERS": {"en": "🪪 The ID of: \n{}"},
    "ID_CHANNEL_OR_GROUP": {
        "en": "🪪 The ID of {} is: `{}`",
    },
    "ID_CHANNELS_OR_GROUPS": {"en": "🪪 The ID of: \n{}"},
    "ID_HIDDEN": {
        "en": "🪪 The ID is hidden. \n{name}",
    },
    "CHOICE_LANG": {"en": "🤳 Select your language."},
    "DONE": {"en": "The selected language is {}"},
    "NOT_HAVE_ID": {
        "en": "❌ The contact you sent has no ID",
    },
    "CAN_NOT_GET_THE_ID": {
        "en": "❌ It is not possible to get the ID of this chat",
    },
    "CHAT_MANAGER": {
        "en": "👮 By clicking the buttons below you can see all the groups and channels you manage and get their ID",
    },
    "REQUEST_CHAT": {"en": "📤 request chat"},
    "INFO_REQUEST_CHAT": {
        "en": "**📤 request chat**\n\n"
        "Click on the buttons below and share the chat whose ID you want to know."
        "\n- In response, the bot will return the ID of the chat you shared",
    },
    "FORWARD": {"en": "⏩ forward"},
    "INFO_FORWARD": {
        "en": "**⏩ forward message**\n\n"
        "Forward any message to the bot (forward with quotes) "
        "and the bot will return the ID of the chat from which the message was sent.",
    },
    "STORY": {"en": "📝 story"},
    "INFO_STORY": {
        "en": "**📝 Story**\n\n" "Transfer a story and get their ID.",
    },
    "SEARCH_USERNAME": {"en": "🔍 username"},
    "INFO_SEARCH_USERNAME": {
        "en": "**🔍 Search by Username**\n\n"
        "Send the username to the bot and the bot will return the ID of the chat with that username.",
    },
    "REPLY_TO_ANOTHER_CHAT": {"en": "↩️ reply to"},
    "INFO_REPLY_TO_ANOTHER_CHAT": {
        "en": "**↩️ Reply to Another Chat**\n\n"
        "Reply to any message in another chat, "
        "and the bot will return the ID of the chat from which the message was replied.",
    },
    "CONTACT": {"en": "🪪 contact"},
    "INFO_CONTACT": {
        "en": "**🪪 Contact**\n\n"
        "Share a contact to the bot and the bot will return the contact's ID to you",
    },
    "REQUEST_ADMIN": {"en": "👮‍♂️ admin"},
    "INFO_REQUEST_ADMIN": {
        "en": "**👮‍ Request Admin**\n\n"
        "Send the command /admin to get all the chats you have name management.",
    },
    "ME": {"en": "👤 me"},
    "INFO_ME": {
        "en": "**👤 Get your ID**\n\n" "Send the command /me to get your ID",
    },
    "LANGUAGE": {"en": "🇺🇸 language"},
    "INFO_LANGUAGE": {
        "en": "**🇺🇸 Language**\n\n" "To change the language send the /lang command.",
    },
    "INFO_GROUP": {
        "en": "**👥 Group**\n\n"
        "Add the bot to the group with the command `/add` "
        "and get the id of the group members with the command `/id`",
    },
    "SHOW_ALL": {"en": "📕 show all"},
    "NEXT": {"en": "next ➡️"},
    "BACK": {"en": "⬅️ back"},
    "MENU": {"en": "🏘 menu"},
    "INFO_MENU": {"en": "🏘 menu help"},
    "ABOUT": {"en": "ℹ️ about"},
    "INFO_ABOUT": {
        "en": "ℹ️ **Details about the bot**\n\n"
        "Language: [Python](https://www.python.org/) \n"
        "Library: [pyrotgfork](https://telegramplayground.github.io/pyrogram/) \n"
        "Bot creator: @TechsCoder 👨‍💻\n\n"
        "Donations: You can support the bot creator with the /donate command\n\n"
        "📢 For updates on the bot, subscribe to @TeleServices_Api,",
    },
    "BUTTON_DEV": {"en": "Send message👨‍💻"},
    "LINK_DEV": {"en": "https://t.me/techscoder"},
    "CHOSE_CHAT_TYPE": {"en": "Choose chat type"},
    "BUTTON_ADD_BOT_TO_GROUP": {"en": "Add bot to group"},
    "ADD_BOT_TO_GROUP": {
        "en": "**Add bot to group**\n\n"
        "Click on the button to add the bot to the group to get id's of members in the group",
    },
    "BOT_ADDED_TO_GROUP": {
        "en": "**Bot added to group**\n\n"
        "The bot was added to the group {group_name} • `{group_id}`\n"
        "to get ids of members in the group, send the command `/id` in the group",
    },
    "BUSINESS": {"en": "🔗 Business connection"},
    "INFO_BUSINESS": {
        "en": "**🔗 Business connection**\n\n"
        "You can connect the bot to your business and get the ID of any chat."
        "\n> Go to settings > Telegram Business > Chatbot > and select this bot"
        "\nThen you can send the command `.id` in any private chat to get the chat ID."
        "\nYou can also get the ID without sending a message in the chat! "
        "\n> Go to the chat and then click on the bot management button "
        "and the bot will send the ID of the chat you came from",
    },
    "BUSINESS_CONNECTION": {
        "en": "**🔗 Business connection**"
        "\nHi, thanks for connecting with me! "
        "\nYou can use me by sending the command `.id` "
        "in any chat (private) to get the chat ID."
        "\n> You can also get the ID without sending a message in the chat! "
        "\n> Go to the chat and then click on the bot management button "
        "and the bot will send the ID of the chat you came from",
    },
    "BUSINESS_CONNECTION_DISABLED": {
        "en": "**🔗 Business connection**"
        "\nI'm sorry, but I can't reply to your messages. "
        "If you want to get the chat ID, enable the permission to reply to messages.",
    },
    "BUSINESS_CONNECTION_REMOVED": {
        "en": "**🔗 Business connection**"
        "\nI'm sorry to see you go, but I'm always here if you need me.",
    },
    "ID_BY_MANAGE_BUSINESS": {
        "en": "🪪 The ID of the chat you came from is: `{}`",
    },
    "ASK_AMOUNT_TO_PAY": {
        "en": "Hi, thanks for wanting to donate to me 🥰\n"
        "Choose the donation amount you want to give 👇",
    },
    "SUPPORT_ME": {
        "en": "Support me 🙏",
    },
    "TEXT_SUPPORT_ME": {
        "en": "Support me with {} ⭐️",
    },
    "PAYMENT_SUCCESS": {
        "en": "🎉 Thank you for your donation 🎉\n" "I received your donation of {} ⭐️",
    },
    "SOMTHING_WENT_WRONG": {
        "en": "Something went wrong",
    },
    "LINK_TO_CHAT": {"en": "🔗 Link to chat `{}`"},
    "BUTTON_GET_LINK": {
        "en": "🔗 Get link",
    },
    "HELLO": {"en": "Hello, welcome to our bot!"},
}


def get_text(*, key: str, lang: str) -> str:
    if default_lang is not None:
        lang = default_lang
    else:
        lang = "he" if lang == "he" else "en"

    try:
        return TEXT[key][lang]
    except KeyError:
        return "Error"
