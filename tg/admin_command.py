import io
import logging
import random
import string
import tempfile
import time
from pyrogram import Client, types, errors

from db import repository
from tg import filters


_logger = logging.getLogger(__name__)


async def stats(_: Client, msg: types.Message):  # command /stats
    """
    Get the stats of the bot.
    """
    users = repository.get_all_users_count()
    users_active = repository.get_users_count_active()
    business = repository.get_users_business_count()

    groups = repository.get_all_groups_count()
    groups_active = repository.get_groups_count_active()

    text = (
    f"**Bot Statistics**\n"
    f"**The number of users subscribed to the bot is:** \n"
    f"Total: {users}\n"
    f"Active: {users_active}\n"
    f"Inactive: {users - users_active}\n"
    f"Business users: {business}\n\n"
    f"**The number of groups in the bot is:** \n"
    f"Total: {groups}\n"
    f"Active: {groups_active}\n"
    f"Inactive: {groups - groups_active}\n"
)


    await msg.reply(text=text, quote=True)


async def ask_for_who_to_send(_: Client, msg: types.Message):
    await msg.reply(
       text="Who would you like to send a message to?",
quote=True,
reply_markup=types.InlineKeyboardMarkup(
    [
        [
            types.InlineKeyboardButton(
                text="To all users", callback_data="send:users"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="To all groups",
                callback_data="send:groups",
            )
        ],
        [types.InlineKeyboardButton(text="Cancel", callback_data="send:no")],
    ]
),


async def asq_message_for_subscribe(_: Client, msg: types.CallbackQuery):
    # Using match to determine the value of send_to
    match send_to := msg.data.split(":")[-1]:
        case "users":
            text = "All users"
        case "groups":
            text = "All groups"
        case "no":
            await msg.answer("The message will not be sent")
            await msg.message.edit_text("Cancelled")
            return
        case _:
            return

    # Reply to the user with a prompt message
    await msg.message.reply(
        text=f"Please send the message you would like to send to {text}\n "
        f"> If the message is forwarded with credit, the bot will also forward it with credit",
    )

    # Add a listener for the action
    filters.add_listener(
        tg_id=msg.from_user.id,
        data={"send_message_to_subscribers": True, "data": send_to},
    )




async def send_broadcast(_: Client, msg: types.Message):
    tg_id = msg.from_user.id
    send_to: str = filters.user_id_to_state.get(tg_id).get("data")

    filters.user_id_to_state.pop(tg_id)

    # users, chats = None, None
    match send_to:
        case "users":
            users = repository.get_all_users_active()
            chats = None
        case "groups":
            chats = repository.get_all_groups_active()
            users = None
        case _:
            return

    log_obj = io.StringIO()

    sent = 0
    failed = 0
    count = 0
    count_edit = 0

    while True:
        sent_id = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        if not repository.is_message_sent_exists(sent_id=sent_id):
            break

    await msg.reply(
    text = f"**📣 Starting to send to:** {len((chats if chats is not None else users))} chats\nPlease wait...\n" \
       f"> Sending identifier: `{sent_id}` can be used to delete the messages sent with the command `/delete {sent_id}`",
)
progress = await msg.reply(text=f"**The message is being sent to:** {sent} chats")


    if users is not None:  # send to users
        for user in users:
            if count > 40:
                count = 0
                time.sleep(3)
            try:
                if msg.forward_origin:
                    msg_sent = await msg.forward(chat_id=user.tg_id)
                else:
                    msg_sent = await msg.copy(chat_id=user.tg_id)
                sent += 1

                repository.create_message_sent(
                    sent_id=sent_id, chat_id=user.tg_id, message_id=msg_sent.id
                )

                if count_edit + 10 == sent:
                    count_edit += 10
                    await progress.edit_text(
                        text=f"**ההודעה נשלחה ל:** {sent} צ'אטים",
                    )

                text_log = (
                    f"sent to user: {user.tg_id}, name: {user.name}, "
                    f"language_code: {user.language_code}, username: {user.username}\n"
                )
                log_obj.write(text_log)
                _logger.debug(text_log)
                count += 1
                time.sleep(
                    0.05
                )  # 20 messages per second (Limit: 30 messages per second)

            except errors.FloodWait as e:
                _logger.error(f"FloodWait: {e.value}")
                time.sleep(e.value)

            except errors.InputUserDeactivated:
                repository.update_user(tg_id=user.tg_id, active=False)
                text_log = (
                    f"user {user.tg_id}, name: {user.name} "
                    f"language_code: {user.language_code}, username: {user.username} is Deactivated\n"
                )
                log_obj.write(text_log)
                _logger.debug(text_log)
                failed += 1
                continue

            except errors.UserIsBlocked:
                repository.update_user(tg_id=user.tg_id, active=False)
                text_log = f"user {user.tg_id}, name: {user.name} language_code: {user.language_code}, username: {user.username} Blocked your bot\n"
                log_obj.write(text_log)
                _logger.debug(text_log)
                failed += 1
                continue

            except errors.PeerIdInvalid:
                repository.update_user(tg_id=user.tg_id, active=False)
                text_log = f"user {user.tg_id}, name: {user.name} language_code: {user.language_code}, username: {user.username} IdInvalid\n"
                log_obj.write(text_log)
                _logger.debug(text_log)
                failed += 1
                continue

            except errors.BadRequest as e:
                repository.update_user(tg_id=user.tg_id, active=False)
                text_log = f"BadRequest: {e} : user {user.tg_id}, name: {user.name} language_code: {user.language_code}, username: {user.username}"
                log_obj.write(text_log)
                _logger.debug(text_log)
                failed += 1
                continue

    if chats is not None:  # send to chats
        for chat in chats:
            if count > 40:
                count = 0
                time.sleep(3)
            try:
                if msg.forward_origin:
                    msg_sent = await msg.forward(chat_id=chat.group_id)
                else:
                    msg_sent = await msg.copy(chat_id=chat.group_id)
                sent += 1

                repository.create_message_sent(
                    sent_id=sent_id, chat_id=chat.group_id, message_id=msg_sent.id
                )

                if count_edit + 10 == sent:
                    count_edit += 10
                    await progress.edit_text(
                        text=f"**The message has been sent to:** {sent} chats",


                text_log = f"sent to user: {chat.group_id}, name: {chat.name} username: {chat.username}\n"
                log_obj.write(text_log)
                _logger.debug(text_log)
                count += 1
                time.sleep(
                    0.05
                )  # 20 messages per second (Limit: 30 messages per second)

            except errors.FloodWait as e:
                _logger.error(f"FloodWait: {e.value}")
                time.sleep(e.value)

            except errors.BadRequest as e:
                repository.update_group(group_id=chat.group_id, active=False)
                text_log = f"BadRequest: {e}, chat_id: {chat.group_id}, name: {chat.name}, username: {chat.username}"
                log_obj.write(text_log)
                _logger.debug(text_log)
                failed += 1
                continue

    text_done = (
    f"📣 The sending is complete\n\n🔹The message was sent to: {sent} chats\n"
    f"🔹The message failed in: {failed} chats"
    f"\n\n🔹Sending identifier: {sent_id}\n"
    f"🔹Sent on: {time.strftime('%d/%m/%Y')}\n"
    f"🔹Sent at: {time.strftime('%H:%M:%S')}\n"
    f"\nYou can delete the messages by sending the command `/delete {sent_id}`"
)


    text_log = f"\n\nSent: {sent}, Failed: {failed}\n Sent_id: {sent_id}\n\n"
    log_obj.write(text_log)
    _logger.debug(text_log)

    with tempfile.TemporaryFile(delete=False) as temp_file:
        # write log to file
        temp_file.write(log_obj.getvalue().encode())
        temp_file.flush()
        temp_file_path = temp_file.name

        try:
            await msg.reply_document(document=temp_file_path, caption=text_done)
        except Exception as e:
            _logger.exception(e)
            await msg.reply(f"```py\n{e}```")


async def delete_sent_messages(client: Client, msg: types.Message):
    """
    Delete sent messages.
    when the user sends the command /delete
    """
    try:
        sent_id = msg.text.split(" ")[1]
    except IndexError:
       await msg.reply("No identifier found for the sent messages")
return

if not repository.is_message_sent_exists(sent_id=sent_id):
    await msg.reply("The identifier is invalid")
    return

sent_messages = repository.get_messages_sent(sent_id=sent_id)
await msg.reply(f"Deleting {len(sent_messages)} sent messages")


    count = 0
    delete = 0
    for sent_message in sent_messages:
        if count > 40:
            count = 0
            time.sleep(3)

        try:
            await client.delete_messages(
                chat_id=sent_message.chat_id, message_ids=sent_message.message_id
            )
            count += 1
            time.sleep(0.05)  # 20 messages per second (Limit: 30 messages per second)
            delete += 1

        except errors.FloodWait as e:
            _logger.error(f"FloodWait: {e.value}")
            time.sleep(e.value)

        except Exception as e:
            _logger.error(
                f"Error: {e}, chat_id: {sent_message.chat_id}, message_id: {sent_message.message_id}"
            )

    await msg.reply(f"{delete} messages were deleted")

