from telethon.tl.functions.users import GetFullUserRequest
from TelethonHell.DB.gvar_sql import addgvar, delgvar, gvarstat
from TelethonHell.plugins import *


@hell_cmd(pattern="sudo$")
async def sudo(event):
    if Config.SUDO_USERS:
        if gvarstat("SUDO_USERS"):
            sudousers = gvarstat("SUDO_USERS")
            await eor(event, f"📍 **ꜱᴜᴅᴏ:**  `Enabled`\n\n📝 **ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ:**  `{sudousers}`")
    else:
        await eod(event, f"📍 **ꜱᴜᴅᴏ:**  `Disabled`")


@hell_cmd(pattern="addsudo(?:\s|$)([\s\S]*)")
async def add(event):
    lists = event.text.split(" ", 1)
    hell = await eor(event, "**✨ ᴡᴀɪᴛ ʙᴀʙy ᴀᴅᴅɪɴɢ ꜱᴜᴅᴏ ᴜꜱᴇʀ...**")
    suu = None
    if len(lists) == 2:
        suu = lists[1].strip()
    reply = await event.get_reply_message()
    if not suu and not reply:
        return await parse_error(hell, "ɴᴏ ᴜꜱᴇʀ ᴍᴇɴᴛɪᴏɴᴇᴅ ᴛᴏ ᴀᴅᴅ ɪɴ ꜱᴜᴅᴏ.")
    if suu and not suu.isnumeric():
        return await parse_error(hell, "ᴏɴʟy ᴜꜱᴇʀ ɪᴅ ɪꜱ ꜱᴜᴩᴩᴏʀᴛᴇᴅ.")
    user = await get_user(event) if reply else suu
    user = str(user)
    if gvarstat("SUDO_USERS"):
        exist = gvarstat("SUDO_USERS")
        int_list = await make_int(exist)
        if int(user) in int_list:
            return await eod(hell, "ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅy ɪɴ ꜱᴜᴅᴏ ʟɪꜱᴛ")
        final = f"{str(exist)} {str(user)}"
    else:
        final = user
    addgvar("SUDO_USERS", final)
    await eod(
        hell,
        f"**ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟy ᴀᴅᴅᴇᴅ ɴᴇᴡ ꜱᴜᴅᴏ ᴜꜱᴇʀ.** \n\n__ʀᴇʟᴏᴀᴅ yᴏᴜʀ ʙᴏᴛ ᴛᴏ ᴀᴩᴩʟy ᴄʜᴀɴɢᴇꜱ. Do__ `{hl}reload`",
    )


@hell_cmd(pattern="rmsudo(?:\s|$)([\s\S]*)")
async def _(event):
    lists = event.text.split(" ", 1)
    hell = await eor(event, "**🚫 ʀᴇᴍᴏᴠɪɴɢ ꜱᴜᴅᴏ ᴜꜱᴇʀ...**")
    reply = await event.get_reply_message()
    suu = None
    if len(lists) == 2:
        suu = lists[1].strip()
    if not suu and not reply:
        return await parse_error(hell, "ɴᴏ ᴜꜱᴇʀ ᴍᴇɴᴛɪᴏɴᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ ꜰʀᴏᴍ ꜱᴜᴅᴏ.")
    if suu and not suu.isnumeric():
        return await parse_error(hell, "Only user id is supported.")
    user = await get_user(event) if reply else suu
    user = str(user)
    if gvarstat("SUDO_USERS"):
        x = gvarstat("SUDO_USERS")
        int_list = await make_int(x)
        if int(user) in int_list:
            int_list.remove(int(user))
            str_list = [str(xyz) for xyz in int_list]
            final = " ".join(str_list)
            delgvar("SUDO_USERS")
            addgvar("SUDO_USERS", final)
            await eod(
                hell,
                f"❌** Removed**  `{str(user)}`  **from Sudo User.**\n\n__Reload your bot to apply changes. Do__ `{hl}reload`",
            )
        else:
            return await eod(hell, "This user is not in your sudo users list.")
    else:
        await eod(hell, "**Sudo Is Disabled !!**")


async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.forward.sender_id)
            )
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.sender_id)
            )
    target = replied_user.users[0].id
    return target


CmdHelp("ꜱᴜᴅᴏ").add_command(
    "sudo", None, "Check If Your Bot Has Sudo Enabled!!"
).add_command(
    "addsudo", "<reply to user>", "Adds replied user to sudo list."
).add_command(
    "rmsudo", "<reply to user>", "Removes the replied user from your sudo list if already added."
).add_info(
    "Manage Sudo."
).add_warning(
    "⚠️ Grant Sudo Access to someone you trust!"
).add()
