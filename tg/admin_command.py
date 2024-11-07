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
        f"**Statistics of the bot**\n"
        f"**Number of users subscribed to the bot:** \n"
        f"Total: {users}\n"
        f"Active: {users_active}\n"
        f"Inactive: {users - users_active}\n"
        f"Business users: {business}\n\n"
        f"**Number of groups in the bot:** \n"
        f"Total: {groups}\n"
        f"Active: {groups_active}\n"
        f"Inactive: {groups - groups_active}\n"
    )

    await msg.reply(text=text, quote=True)

async def ask_for_who_to_send(_: Client, msg: types.Message):
    await msg.reply(
        text="To whom would you like to send a message?",
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
    )

async def asq_message_for_subscribe(_: Client, msg: types.CallbackQuery):
    match send_to := msg.data.split(":")[-1]:
        case "users":
            send_to = send_to
            text = "all users"
        case "groups":
            send_to = send_to
            text = "all groups"
        case "no":
            await msg.answer("The message will not be sent")
            await msg.message.edit_text("Canceled")
            return
        case _:
            return

    await msg.message.reply(
        text=f"Please send the message you want to send to {text}\n "
        f"> If the message is forwarded with credit, the bot will also forward it with credit",
    )
    filters.add_listener(
        tg_id=msg.from_user.id,
        data={"send_message_to_subscribers": True, "data": send_to},
    )

async def send_broadcast(_: Client, msg: types.Message):
    tg_id = msg.from_user.id
    send_to: str = filters.user_id_to_state.get(tg_id).get("data")

    filters.user_id_to_state.pop(tg_id)

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
        text=f"**📣 Starting to send to:** {len((chats if chats is not None else users))} chats\nPlease wait...\n"
        f"> Sending ID: `{sent_id}` can be used to delete the sent messages with the command `/delete {sent_id}`",
    )
    progress = await msg.reply(text=f"**Message sent to:** {sent} chats")

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
                        text=f"**Message sent to:** {sent} chats",
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
                        text=f"**Message sent to:** {sent} chats",
                    )

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
        f"📣 Sending completed\n\n🔹Message sent to: {sent} chats\n"
        f"🔹 Message failed in: {failed} chats"
        f"\n\n🔹 Sending ID: {sent_id}\n"
        f"🔹 Sent on: {time.strftime('%d/%m/%Y')}\n"
        f"🔹 Sent at: {time.strftime('%H:%M:%S')}\n"
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
    try:
        sent_id = msg.text.split(" ", maxsplit=1)[-1]
    except Exception as e:
        await msg.reply(text=f"Error: {e}")
        return

    data = repository.get_messages_sent(sent_id=sent_id)
    if not data:
        await msg.reply(text="No sent messages found in the database")
        return

    delete_progress = await msg.reply(text=f"**Deleting sent messages**\nStarting...")
    deleted = 0
    failed = 0
    for row in data:
        try:
            await client.delete_messages(chat_id=row.chat_id, message_ids=row.message_id)
            repository.delete_message_sent(sent_id=sent_id, chat_id=row.chat_id, message_id=row.message_id)
            deleted += 1
            time.sleep(0.05)  # Sleep between deletions to avoid rate limiting

        except errors.FloodWait as e:
            await msg.reply(text=f"FloodWait of {e.value} seconds")
            time.sleep(e.value)
            failed += 1
            continue
        except errors.BadRequest as e:
            await msg.reply(text=f"BadRequest: {e}")
            failed += 1
            continue

    await delete_progress.edit_text(
        text=f"**Deletion completed**\n\n🔹 Deleted: {deleted} messages\n🔹 Failed: {failed} messages"
    )
