from dataclasses import dataclass, field
import discord
import google.cloud.firestore_v1.client
from typing import Dict


class Config:
    guild: discord.Guild = None
    db: google.cloud.firestore_v1.client.Client = None

    class Minecraft_Server_Path:
        prod_path = "/usr/local/a2cmc/whitelist.json"
        prod = True  # If true, will use the prod_path, else will use the dev_path

    class ServerIDs:
        test_server = 940047935499042826
        main_server = 786557653924708373

    class UserIDs:
        admins = [342878563411820544]  # carly or other admin
        mods = [173636229982584832]  # Abnon
        admidral = 262424335032123394
        devs = [557086321219469324, 378916678056280065]  # koala, spencillian

    class RoleIDs:

        # Unprotected list of roles
        mod = 940047935763284081
        roles = []
        # Staff Roles
        admin = 800996919114596362
        server_moderator = 786557879288463360
        mod_in_training = 940047935763284079
        dev = 866737213403693056

        GradeLevel = []
        Pronouns = []
        DMStatus = []
        ApplicationType = []
        EducationType = []
        Region = []
        Interests = []

    class ChannelIDs:
        general = None
        emoji_suggestions = None
        suggestion_decisions = None
        suggestion_voting = None
        bot_commands = None
        roles = None
        dev_chat = None
        college_talk = None
        app_discussion = None
        extracurriculars = None
        reports: discord.TextChannel = None
        days_old_channel = None

    class Slowmode:
        @dataclass
        class ChannelConfig:
            increment: int
            cap: int
            message_rate: float
            apply_to_threads: bool = True
            last_messages: int = 0
            threads_last_messages: Dict[str, int] = field(default_factory=dict)
            
        channels: Dict[str, ChannelConfig] = {}
        threads: Dict[str, ChannelConfig] = {}

    class Emojis:
        arrow_up = '⬆️'
        arrow_down = '⬇️'

    class BotSettings:
        delete_delay = 15
